from discord import Embed

from src.kiyomi import Kiyomi
from .leaderboard_cog import LeaderboardCog
from .message import Message
from .services import PlayerLeaderboardService, PlayerScoreLeaderboard, PlayerTopScoresLeaderboard
from .storage import UnitOfWork


class LeaderboardAPI(LeaderboardCog):
    def __init__(self, bot: Kiyomi, player_leaderboard_service: PlayerLeaderboardService, uow: UnitOfWork):
        super().__init__(bot, player_leaderboard_service)

        self.uow = uow

    async def get_player_score_leaderboard(self, guild_id: int, beatmap_key: str) -> PlayerScoreLeaderboard:
        return await self.player_leaderboard_service.get_player_score_leaderboard_by_guild_id_and_beatmap_key(guild_id, beatmap_key)

    async def get_player_score_leaderboard_embed(self, guild_id: int, beatmap_key: str) -> Embed:
        leaderboard = await self.get_player_score_leaderboard(guild_id, beatmap_key)

        return Message.get_player_score_leaderboard_embed(leaderboard)

    def get_player_top_scores_leaderboard(self, player_id: str) -> PlayerTopScoresLeaderboard:
        return self.player_leaderboard_service.get_player_top_scores_leaderboard(player_id)
