from sqlalchemy.ext.asyncio import AsyncSession

from .repository.message_view_repository import MessageViewRepository
from kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.message_views = MessageViewRepository(self._session)
