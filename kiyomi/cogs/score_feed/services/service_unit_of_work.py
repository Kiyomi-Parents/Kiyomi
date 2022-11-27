from .notification_service import NotificationService
from .sent_score_service import SentScoreService
from ..storage import StorageUnitOfWork
from kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.sent_scores = SentScoreService(bot, storage_uow.sent_scores, storage_uow)
        self.notifications = NotificationService(bot, storage_uow, self.sent_scores)
