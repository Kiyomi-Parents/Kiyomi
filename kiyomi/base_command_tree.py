from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, InteractionType
from discord.app_commands import CommandTree, AppCommandError, Namespace
from discord.ext.commands import Context, Cog

if TYPE_CHECKING:
    pass


class BaseCommandTree(CommandTree["Kiyomi"]):
    async def on_error(self, interaction: Interaction, error: AppCommandError) -> None:
        ctx = await Context.from_interaction(interaction)

        command = ctx.command
        if command is not None:

            cog = command.binding
            if cog is not None and isinstance(cog, Cog):
                # Call Cog Global error handler
                if cog.has_error_handler():
                    await cog.cog_command_error(ctx=ctx, error=error)

        # Call Bot Global error handler
        await ctx.bot.on_command_error(ctx, error)

    async def call(self, interaction: Interaction) -> None:
        if not await self.interaction_check(interaction):
            return

        data: ApplicationCommandInteractionData = interaction.data  # type: ignore
        type = data.get('type', 1)
        if type != 1:
            # Context menu command...
            await self._call_context_menu(interaction, data, type)
            return

        command, options = self._get_app_command_options(data)

        # Pre-fill the cached slot to prevent re-computation
        interaction._cs_command = command

        # At this point options refers to the arguments of the command
        # and command refers to the class type we care about
        namespace = Namespace(interaction, data.get('resolved', {}), options)

        # Same pre-fill as above
        interaction._cs_namespace = namespace

        # Auto complete handles the namespace differently... so at this point this is where we decide where that is.
        if interaction.type is InteractionType.autocomplete:
            focused = next((opt['name'] for opt in options if opt.get('focused')), None)
            if focused is None:
                raise AppCommandError('This should not happen, but there is no focused element. This is a Discord bug.')
            await command._invoke_autocomplete(interaction, focused, namespace)
            return

        cog = command.binding

        try:
            if cog is not None and isinstance(cog, Cog):
                await cog.cog_before_invoke(await Context.from_interaction(interaction))

            await command._invoke_with_namespace(interaction, namespace)
        except AppCommandError as e:
            await command._invoke_error_handlers(interaction, e)
            await self.on_error(interaction, e)

        finally:
            if cog is not None and isinstance(cog, Cog):
                await cog.cog_after_invoke(await Context.from_interaction(interaction))
