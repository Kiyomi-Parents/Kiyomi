from discord.ext import commands

from .actions import Actions
from .message import Message
from .storage.uow import UnitOfWork
from src.base.base_cog import BaseCog


class Leaderboard(BaseCog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):
        pass

    @commands.command()
    async def song_leaderboard(self, ctx, key: str):
        """Displays song leaderboard."""
        leaderboard = await self.actions.get_player_score_leaderboard_by_guild_id_and_beatmap_key(ctx.guild.id, key)

        guild_leaderboard_embed = Message.get_player_score_leaderboard_embed(leaderboard)
        await ctx.send(embed=guild_leaderboard_embed)
