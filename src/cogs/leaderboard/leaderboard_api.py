from discord import Embed
from discord.ext import commands

from .actions import Actions, PlayerScoreLeaderboard
from .message import Message
from .storage.uow import UnitOfWork


class LeaderboardAPI(commands.Cog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    def get_player_score_leaderboard(self, guild_id: int, beatmap_key: str) -> PlayerScoreLeaderboard:
        return self.actions.get_player_score_leaderboard_by_guild_id_and_beatmap_key(guild_id, beatmap_key)

    def get_player_score_leaderboard_embed(self, guild_id: int, beatmap_key: str) -> Embed:
        leaderboard = self.get_player_score_leaderboard(guild_id, beatmap_key)

        return Message.get_player_score_leaderboard_embed(leaderboard)
