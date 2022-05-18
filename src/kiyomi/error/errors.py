from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING

from discord import Interaction, DiscordException
from discord.app_commands import AppCommandError
from discord.ext.commands import Context

from src.kiyomi.error.error_embed import ErrorEmbed
from src.kiyomi.error.error_resolver import ErrorResolver
from src.kiyomi.error.error_utils import send_exception
from src.log import Logger

if TYPE_CHECKING:
    from src.kiyomi.kiyomi import Kiyomi


class KiyomiException(DiscordException):
    is_handled: bool = False

    def _log(self, message: Optional[str] = None):
        if message is None:
            message = str(self)

        Logger.error(self.__class__.__name__, message)

    async def _respond(
        self,
        ctx: Union[Context["Kiyomi"], Interaction],
        message: Optional[str] = None,
        **options,
    ):
        if message is None:
            message = str(self)

        error_embed = ErrorEmbed(message)

        await send_exception(ctx, embed=error_embed, ephemeral=True, **options)

    async def handle(self, **options):
        if self.is_handled:
            return

        message = options.pop("message") if "message" in options.keys() else str(self)

        message_detailed = ErrorResolver.resolve_message_simple(self, message, True)
        self._log(message_detailed)

        ctx: Optional[Union[Context["Kiyomi"], Interaction]] = options.pop("ctx") if "ctx" in options.keys() else None

        if ctx is not None:
            message_simple = ErrorResolver.resolve_message_simple(self, message, True)
            await self._respond(ctx, message_simple, **options)

        self.is_handled = True


class CogException(KiyomiException):
    async def handle(self, **options):
        if self.is_handled:
            return

        bot: Optional["Kiyomi"] = options.pop("bot") if "bot" in options.keys() else None

        if bot is None:
            Logger.warn(
                f"{self.__class__.__name__}",
                "bot parameter not included! Please include for better messages!",
            )
            return await super().handle(**options)

        message: str = options.pop("message") if "message" in options.keys() else str(self)

        message_detailed = await bot.error_resolver.resolve_message(self, message, True)
        self._log(message_detailed)

        ctx: Optional[Union[Context["Kiyomi"], Interaction]] = options.pop("ctx") if "ctx" in options.keys() else None

        if ctx is not None:
            message_simple = await bot.error_resolver.resolve_message(self, message, False)
            await self._respond(ctx, message_simple, **options)

        self.is_handled = True


class CommandError(CogException, AppCommandError):
    pass


class BadArgument(CommandError):
    def __init__(self, ctx: Interaction, argument: str) -> None:
        self.ctx = ctx
        self.argument = argument

        super().__init__(str(self))

    def __str__(self):
        argument_name = self.find_command_argument_name()

        if argument_name is None:
            return f"Bad argument **{self.argument}**"
        else:
            return f"Bad argument {argument_name}: **{self.argument}**"

    def find_command_argument_name(self) -> Optional[str]:
        if isinstance(self.ctx, Interaction):
            selected_option = self.find_command_by_argument_autocomplete_context(self.ctx)
            if selected_option is not None:
                return selected_option[0]

        return None

    def find_command_by_argument_autocomplete_context(self, ctx: Interaction) -> Optional[tuple[str, Union[str, None]]]:
        for key, value in ctx.namespace:
            if value == self.argument or (value.isspace() and self.argument is None):
                return key, value

        return None


class CheckFailure(CommandError):
    pass


class OwnerOnlyCommand(CheckFailure):
    def __str__(self):
        return f"This command can only be used by the bot owners!"
