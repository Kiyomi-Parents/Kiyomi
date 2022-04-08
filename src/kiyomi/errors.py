from typing import Optional, Dict, Union

from discord import ApplicationContext, AutocompleteContext


class KiyomiException(Exception):
    is_handled: bool = False

    async def handle(self, ctx: ApplicationContext, message: Optional[str] = None, **kwargs):
        if self.is_handled:
            return

        if message is None:
            message = str(self)

        await ctx.respond(message, ephemeral=True, **kwargs)

        self.is_handled = True


class CogException(KiyomiException):
    pass


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
