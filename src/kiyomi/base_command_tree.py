from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction
from discord.app_commands import CommandTree, AppCommandError
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

