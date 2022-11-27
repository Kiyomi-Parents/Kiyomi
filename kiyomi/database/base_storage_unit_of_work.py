import logging
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from ..base_unit_of_work import BaseUnitOfWork

TEntity = TypeVar("TEntity")
_logger = logging.getLogger(__name__)


class BaseStorageUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def refresh(self, entity: TEntity) -> TEntity:
        _logger.debug(entity, "Refreshing entity")

        await self._session.refresh(entity)
        return entity

    async def commit(self):
        _logger.debug("Committing changes")

        await self._session.commit()

    async def rollback(self):
        _logger.debug("Rolling back changes")

        await self._session.rollback()

    async def close(self):
        _logger.debug("Closing session")

        await self._session.close()

    async def save_changes(self):
        try:
            await self.commit()
        except Exception as error:
            _logger.error(f"Transaction failed: {error}")
            await self.rollback()
