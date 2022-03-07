from discord import slash_command
from discord.ext import commands

from src.cogs.settings.storage.model.ToggleSetting import ToggleSetting
from src.kiyomi.base_cog import BaseCog
from .actions import Actions
from .message import Message
from .storage.uow import UnitOfWork


class Leaderboard(BaseCog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ToggleSetting.create("map_leaderboard", False)
        ]

        self.uow.bot.events.emit("setting_register", settings)

    @slash_command()
    async def song_leaderboard(self, ctx, key: str):
        """Displays song leaderboard."""
        leaderboard = await self.actions.get_player_score_leaderboard_by_guild_id_and_beatmap_key(ctx.guild.id, key)

        guild_leaderboard_embed = Message.get_player_score_leaderboard_embed(leaderboard)
        await ctx.respond(embed=guild_leaderboard_embed)
