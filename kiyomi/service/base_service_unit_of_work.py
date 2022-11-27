from typing import TypeVar, Generic

from ..base_unit_of_work import BaseUnitOfWork
from ..database.base_storage_unit_of_work import BaseStorageUnitOfWork

TEntity = TypeVar("TEntity")
TStorageUnitOfWork = TypeVar("TStorageUnitOfWork", bound=BaseStorageUnitOfWork)


class BaseServiceUnitOfWork(BaseUnitOfWork, Generic[TStorageUnitOfWork]):
    def __init__(self, storage_uow: TStorageUnitOfWork):
        self._storage_uow = storage_uow

    async def refresh(self, entry: TEntity) -> TEntity:
        return await self._storage_uow.refresh(entry)

    async def commit(self):
        await self._storage_uow.commit()

    async def rollback(self):
        await self._storage_uow.rollback()

    async def close(self):
        await self._storage_uow.close()

    async def save_changes(self):
        await self._storage_uow.save_changes()
