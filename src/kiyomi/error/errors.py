from __future__ import annotations

from typing import Optional, Dict, Union, TypeVar, Generic, TYPE_CHECKING

from discord import ApplicationContext, AutocompleteContext

from src.log import Logger

if TYPE_CHECKING:
    pass


class KiyomiException(Exception):
    is_handled: bool = False

    def _log(self, message: Optional[str] = None):
        if message is None:
            message = str(self)

        Logger.error(self.__class__.__name__, message)

    async def _respond(self, ctx: ApplicationContext, message: Optional[str] = None, **options):
        if message is None:
            message = str(self)

        await ctx.respond(message, ephemeral=True, **options)

    async def handle(self, **options):
        if self.is_handled:
            return

        message = options.pop("message") if "message" in options.keys() else str(self)
        self._log(message)

        ctx: Optional[ApplicationContext] = options.pop("ctx")

        if ctx is not None:
            await self._respond(ctx, message, **options)

        self.is_handled = True


TCog = TypeVar("TCog", bound="BaseCog")


class CogException(KiyomiException, Generic[TCog]):

    async def handle(self, **options):
        if self.is_handled:
            return

        cog: TCog = options.pop("cog")

        if cog is None:
            Logger.warn(f"{self.__class__.__name__}", "cog parameter not included! Please include for better messages!")
            return await super().handle(**options)

        message: str = options.pop("message") if "message" in options.keys() else str(self)

        message_detailed = await cog.bot.error_resolver.resolve_message(self, message)
        self._log(message_detailed)

        ctx: Optional[ApplicationContext] = options.pop("ctx")

        if ctx is not None:
            message_simple = await cog.bot.error_resolver.resolve_message(self, message)
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
