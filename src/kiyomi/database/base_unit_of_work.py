from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession


class BaseUnitOfWork:
    _session: AsyncSession

    def __init__(self, session_maker: Callable[[], AsyncSession]):
        self._session_maker = session_maker

    async def start(self):
        self._session = self._session_maker()

    async def save_changes(self):
        await self._session.commit()
