import logging
from abc import ABCMeta
from datetime import datetime, timedelta
from typing import List, Optional, TypeVar, Generic, Dict

from sqlalchemy import select, exists, update, delete

from kiyomi import Base
from kiyomi.database import BaseStorageRepository

TEntity = TypeVar("TEntity", bound=Base)
_logger = logging.getLogger(__name__)

class BaseCacheableRepository(BaseStorageRepository[TEntity], Generic[TEntity], metaclass=ABCMeta):

    @property
    def _expire_threshold(self) -> datetime:
        return datetime.today() - timedelta(days=30)

    async def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        stmt = (
            select(self._table)
            .where(self._table.id == entity_id)
            .where(self._table.cached_at >= self._expire_threshold)
        )
        return await self._first(stmt)

    async def get_cached_by_id(self, entity_id: int) -> Optional[TEntity]:
        return await super(BaseCacheableRepository, self).get_by_id(entity_id)

    async def get_all(self) -> List[TEntity]:
        stmt = (
            select(self._table)
            .where(self._table.cached_at >= self._expire_threshold)
        )
        results = await self._all(stmt)

        return results

    async def exists(self, entity_id: int) -> bool:
        stmt = (
            select(self._table)
            .where(self._table.id == entity_id)
            .where(self._table.cached_at >= self._expire_threshold)
        )
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()

    async def is_cached(self, entity_id: int) -> bool:
        return await super(BaseCacheableRepository, self).exists(entity_id)

    async def add(self, entity: TEntity) -> TEntity:
        if await self.is_cached(entity.id):
            rehydrated_entity = await self.update_entity(entity)
            _logger.info(rehydrated_entity, "Rehydrated cache")

            return rehydrated_entity
        else:
            self._session.add(entity)
            _logger.info(entity, "Cached")


        return entity

    async def add_all(self, entities: List[TEntity]) -> List[TEntity]:
        for entity in entities:
            await self.add(entity)

        _logger.info(type(entities[0]).__name__, f"Cached {len(entities)} new entries")
        return entities

    async def remove_by_id(self, entity_id: int) -> Optional[TEntity]:
        entity = await self.get_cached_by_id(entity_id)
        stmt = delete(self._table).where(self._table.id == entity_id)
        await self._session.execute(stmt)

        _logger.info(entity, "Removed")
        return entity

    async def update(self, entity_id: int, values: Dict[str, any]) -> TEntity:
        entity = await self.get_cached_by_id(entity_id)
        stmt = update(self._table).where(self._table.id == entity_id).values(values)

        await self._session.execute(stmt)

        _logger.info(entity, "Updated")
        return entity