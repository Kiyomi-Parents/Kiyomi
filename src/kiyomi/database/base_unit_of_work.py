from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseUnitOfWork:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self):
        return self
        # return await self._session.begin()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        # await self._session.close()

    async def refresh(self, entry: T):
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
