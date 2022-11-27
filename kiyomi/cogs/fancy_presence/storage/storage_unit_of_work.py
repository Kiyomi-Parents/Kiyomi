from sqlalchemy.ext.asyncio import AsyncSession

from kiyomi.cogs.fancy_presence.storage.repository.presence_repository import (
    PresenceRepository,
)
from kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.presences = PresenceRepository()
