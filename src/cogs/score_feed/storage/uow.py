from Kiyomi import Kiyomi
from .repository.sent_score_repository import SentScoreRepository


class UnitOfWork:

    def __init__(self, bot: Kiyomi):
        self.sent_score_repo = SentScoreRepository(bot.database)

        self.bot = bot
