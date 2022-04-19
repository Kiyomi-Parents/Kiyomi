from __future__ import annotations

from typing import Optional, Dict, Union, TYPE_CHECKING

from discord import ApplicationContext, AutocompleteContext

from src.kiyomi.error.error_embed import ErrorEmbed
from src.kiyomi.error.error_resolver import ErrorResolver
from src.log import Logger

if TYPE_CHECKING:
    from src.kiyomi.kiyomi import Kiyomi


class KiyomiException(Exception):
    is_handled: bool = False

    def _log(self, message: Optional[str] = None):
        if message is None:
            message = str(self)

        Logger.error(self.__class__.__name__, message)

    async def _respond(self, ctx: ApplicationContext, message: Optional[str] = None, **options):
        if message is None:
            message = str(self)

        error_embed = ErrorEmbed(message)

        await ctx.respond(embed=error_embed, ephemeral=True, **options)

    async def handle(self, **options):
        if self.is_handled:
            return

        message = options.pop("message") if "message" in options.keys() else str(self)

        message_detailed = ErrorResolver.resolve_message_simple(self, message, True)
        self._log(message_detailed)

        ctx: Optional[ApplicationContext] = options.pop("ctx") if "ctx" in options.keys() else None

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
            Logger.warn(f"{self.__class__.__name__}", "bot parameter not included! Please include for better messages!")
            return await super().handle(**options)

        message: str = options.pop("message") if "message" in options.keys() else str(self)

        message_detailed = await bot.error_resolver.resolve_message(self, message, True)
        self._log(message_detailed)

        ctx: Optional[ApplicationContext] = options.pop("ctx") if "ctx" in options.keys() else None

        if ctx is not None:
            message_simple = await bot.error_resolver.resolve_message(self, message, False)
            await self._respond(ctx, message_simple, **options)

        self.is_handled = True


class CommandError(KiyomiException):
    pass


class BadArgument(CommandError):
    def __init__(self, ctx: ApplicationContext, argument: str) -> None:
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
        if isinstance(self.ctx, ApplicationContext):
            selected_option = self.find_command_by_argument_application_context(self.ctx)
            return selected_option.get("name")
        elif isinstance(self.ctx, AutocompleteContext):
            selected_option = self.find_command_by_argument_autocomplete_context(self.ctx)
            return selected_option[0]

        return None

    def find_command_by_argument_application_context(self, ctx: ApplicationContext) -> Optional[Dict]:
        for selected_option in ctx.selected_options:
            if selected_option.get("value") == self.argument:
                return selected_option

        return None

    def find_command_by_argument_autocomplete_context(
            self,
            ctx: AutocompleteContext
    ) -> Optional[tuple[str, Union[str, None]]]:
        for key, value in ctx.options.items():
            if value == self.argument:
                return key, value

        return None
