from .services import PlayerService, ScoreService
from src.kiyomi import BaseCog, Kiyomi


class ScoreSaberCog(BaseCog):
    def __init__(self, bot: Kiyomi, player_service: PlayerService, score_service: ScoreService):
        super().__init__(bot)

        self.player_service = player_service
        self.score_service = score_service
