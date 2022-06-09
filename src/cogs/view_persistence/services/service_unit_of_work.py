from ..storage import StorageUnitOfWork
from .message_view_service import MessageViewService
from src.kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.message_views = MessageViewService(bot, storage_uow.message_views, storage_uow)
