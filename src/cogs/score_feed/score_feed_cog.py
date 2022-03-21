from .services import SentScoreService, NotificationService
from src.kiyomi import BaseCog, Kiyomi


class ScoreFeedCog(BaseCog):
    def __init__(self, bot: Kiyomi, notification_service: NotificationService, sent_score_service: SentScoreService):
        super().__init__(bot)

        self.notification_service = notification_service
        self.sent_score_service = sent_score_service
