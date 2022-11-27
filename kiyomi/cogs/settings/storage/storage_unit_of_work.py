from sqlalchemy.ext.asyncio import AsyncSession

from kiyomi.database import BaseStorageUnitOfWork
from .repository.settings_repository import SettingRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.settings_repo = SettingRepository(self._session)
