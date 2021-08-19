from pydoc import locate

from discord.ext import commands

from .actions import Actions
from .storage.uow import UnitOfWork
from src.cogs.security import Security
from src.kiyomi.base_cog import BaseCog


class Settings(BaseCog):

    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    @commands.group(invoke_without_command=True)
    @Security.owner_or_permissions(administrator=True)
    async def settings(self, ctx):
        """Link ScoreSaber profile to Discord member."""
        await ctx.send_help(ctx.command)

    @settings.command(name="set")
    async def settings_set(self, ctx, setting_name: str, value_type: str, setting_value: str):
        """Set setting value"""
        t = locate(value_type)
        value = t(setting_value)
        self.actions.set(ctx.guild.id, setting_name, value)

    @settings.command(name="get")
    async def settings_get(self, ctx, setting_name: str):
        """Get setting value"""
        setting_value = self.actions.get_value(ctx.guild.id, setting_name)
        await ctx.send(f"{setting_name} = {setting_value}")

    # TODO: Find a better way for this. This should belong in BeatSaver cog!
    @settings.command(name="leaderboard")
    async def settings_leaderboard(self, ctx, status: str):
        """Enable/Disable leaderboards on map command."""
        if status.lower() == "enable":
            self.actions.set(ctx.guild.id, "map_leaderboard", True)
        elif status.lower() == "disable":
            self.actions.set(ctx.guild.id, "map_leaderboard", False)
        else:
            await ctx.send(f"Only valid options are: enable, disable")

        await ctx.send(f"Map leaderboards are now: {status}")

