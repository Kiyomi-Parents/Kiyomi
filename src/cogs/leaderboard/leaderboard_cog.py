from src.kiyomi import BaseCog, Kiyomi
from .services import PlayerLeaderboardService


class LeaderboardCog(BaseCog):
    def __init__(self, bot: Kiyomi, player_leaderboard_service: PlayerLeaderboardService):
        super().__init__(bot)

        self.player_leaderboard_service = player_leaderboard_service
