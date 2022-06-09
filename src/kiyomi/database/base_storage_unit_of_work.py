from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from ..base_unit_of_work import BaseUnitOfWork

TEntity = TypeVar("TEntity")


class BaseStorageUnitOfWork(BaseUnitOfWork):
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def refresh(self, entry: TEntity) -> TEntity:
        return await self._session.refresh(entry)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def save_changes(self):
        try:
            await self._session.commit()
        except Exception as error:
            await self._session.rollback()
            raise error
