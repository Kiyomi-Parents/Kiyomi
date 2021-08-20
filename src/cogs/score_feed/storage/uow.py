from Kiyomi import Kiyomi
from .repository.sent_score_repository import SentScoreRepository
from ...scoresaber.storage.repository.player_repository import PlayerRepository
from ...scoresaber.storage.repository.score_repository import ScoreRepository


class UnitOfWork:

    def __init__(self, bot: Kiyomi):
        self.sent_score_repo = SentScoreRepository(bot.database)
        self.score_repo = ScoreRepository(bot.database)
        self.player_repo = PlayerRepository(bot.database)

        self.bot = bot
