import logging
from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Optional, List, Type, Dict

from sqlalchemy import select, exists, delete, update
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable

from .database import Base
from ..base_repository import BaseRepository
from ..utils import Utils

TEntity = TypeVar("TEntity", bound=Base)
_logger = logging.getLogger(__name__)


class BaseStorageRepository(BaseRepository[TEntity], Generic[TEntity], metaclass=ABCMeta):
    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    @abstractmethod
    def _table(self) -> Type[TEntity]:
        pass

    async def _execute_scalars(self, stmt: Executable) -> ScalarResult:
        result = await self._session.execute(stmt)
        return result.scalars()

    async def _first(self, stmt: Executable) -> Optional[TEntity]:
        result = await self._execute_scalars(stmt)
        return result.first()

    async def _all(self, stmt: Executable) -> List[TEntity]:
        result = await self._execute_scalars(stmt)
        return result.unique().all()

    async def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        stmt = select(self._table).where(self._table.id == entity_id)
        return await self._first(stmt)

    async def get_all(self) -> List[TEntity]:
        stmt = select(self._table)
        return await self._all(stmt)

    async def exists(self, entity_id: int) -> bool:
        stmt = select(self._table).where(self._table.id == entity_id)
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()

    async def add(self, entity: TEntity) -> TEntity:
        self._session.add(entity)

        _logger.info(entity, "Added")
        return entity

    async def add_all(self, entities: List[TEntity]) -> List[TEntity]:
        self._session.add_all(entities)

        _logger.info(type(entities[0]).__name__, f"Added {len(entities)} new entries")
        return entities

    async def remove(self, entity: TEntity) -> TEntity:
        await self._session.delete(entity)

        _logger.info(entity, "Removed")
        return entity

    async def remove_by_id(self, entity_id: int) -> Optional[TEntity]:
        entity = await self.get_by_id(entity_id)
        stmt = delete(self._table).where(self._table.id == entity_id)
        await self._session.execute(stmt)

        _logger.info(entity, "Removed")
        return entity

    async def upsert(self, entity: TEntity) -> TEntity:
        if await self.exists(entity.id):
            return await self.update_entity(entity)

        return await self.add(entity)

    async def update(self, entity_id: int, values: Dict[str, any]) -> TEntity:
        entity = await self.get_by_id(entity_id)
        stmt = update(self._table).where(self._table.id == entity_id).values(values)

        await self._session.execute(stmt)

        _logger.info(entity, "Updated")
        return entity

    async def update_entity(self, entity: TEntity) -> TEntity:
        return await self.update(entity.id, Utils.get_class_fields(entity))
