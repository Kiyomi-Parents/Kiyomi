from sqlalchemy.ext.asyncio import AsyncSession

from src.cogs.fancy_presence.storage.repository.presence_repository import (
    PresenceRepository,
)
from src.kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.presences = PresenceRepository()