import logging
from abc import abstractmethod
from typing import Generic, TypeVar, TYPE_CHECKING

import sentry_sdk
from discord import Interaction, app_commands
from discord.app_commands import CommandInvokeError, TransformerError
from discord.ext import commands
from discord.ext.commands import Context, CogMeta
from termcolor import colored

from .service import BaseServiceUnitOfWork
from .error import KiyomiException, CogException

if TYPE_CHECKING:
    from .kiyomi import Kiyomi

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)
_logger = logging.getLogger(__name__)


class BaseCog(commands.Cog, Generic[TServiceUOW], metaclass=CogMeta):
    def __init__(self, bot: "Kiyomi", service_uow: TServiceUOW):
        self.bot = bot
        self._service_uow = service_uow

        self.register_events()

    @abstractmethod
    def register_events(self):
        pass

    async def cog_before_invoke(self, ctx: Context["Kiyomi"]):
        sentry_sdk.start_transaction(name=ctx.command.qualified_name)
        command_args = [f"{key}: {value}" for key, value in ctx.interaction.namespace]

        _logger.info(
            self.qualified_name,
            f"{colored(ctx.interaction.user.name, 'blue')} executed command "
            f"{colored('/' + ctx.command.qualified_name, 'blue')} "
            f"{colored(''.join(command_args), 'cyan')} in "
            f"{colored(f'#{ctx.interaction.channel.name}', 'blue')} at "
            f"{colored(ctx.interaction.guild.name, 'blue')}",
        )

    async def cog_after_invoke(self, ctx: Context["Kiyomi"]) -> None:
        await self._service_uow.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._service_uow.save_changes()
        await self._service_uow.close()

    async def cog_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, KiyomiException):
            if error.is_handled:
                return

        if isinstance(error, CogException):
            return await error.handle(ctx=interaction, bot=self.bot)

    async def cog_command_error(self, ctx: Context["Kiyomi"], error: Exception):
        if isinstance(error, TransformerError):
            error = error.__cause__

        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, KiyomiException):
            if error.is_handled:
                return

        if isinstance(error, CogException):
            return await error.handle(ctx=ctx, bot=self.bot)
