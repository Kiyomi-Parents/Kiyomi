from sqlalchemy.ext.asyncio import AsyncSession

from kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
