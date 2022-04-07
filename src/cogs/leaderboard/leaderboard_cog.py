from src.kiyomi import BaseCog, Kiyomi
from .services import PlayerLeaderboardService
from .services.score_leaderboard_service import ScoreLeaderboardService


class LeaderboardCog(BaseCog):
    def __init__(self, bot: Kiyomi, player_leaderboard_service: PlayerLeaderboardService, score_leaderboard_service: ScoreLeaderboardService):
        super().__init__(bot)

        self.player_leaderboard_service = player_leaderboard_service
        self.score_leaderboard_service = score_leaderboard_service
