from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession

from src.kiyomi.database import BaseStorageUnitOfWork
from .repository.settings_repository import SettingRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.settings_repo = SettingRepository(self._session)
