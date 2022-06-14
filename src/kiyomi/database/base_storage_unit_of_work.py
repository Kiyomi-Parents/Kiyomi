from typing import TypeVar, Optional

from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession

from ..base_unit_of_work import BaseUnitOfWork

TEntity = TypeVar("TEntity")


class BaseStorageUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def refresh(self, entity: TEntity) -> TEntity:
        await self._session.refresh(entity)
        return entity

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()

    async def save_changes(self):
        try:
            await self._session.commit()
        except Exception as error:
            await self._session.rollback()
            raise error
