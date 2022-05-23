from src.kiyomi import BaseCog, Kiyomi
from .services import SentScoreService, NotificationService


class ScoreFeedCog(BaseCog):
    def __init__(
        self,
        bot: Kiyomi,
        notification_service: NotificationService,
        sent_score_service: SentScoreService,
    ):
        super().__init__(bot)

        self.notification_service = notification_service
        self.sent_score_service = sent_score_service
