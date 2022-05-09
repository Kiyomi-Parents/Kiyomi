from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Optional, List, Type

from sqlalchemy import select, exists, delete, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable

from src.log import Logger
from .database import Base
from ..utils import Utils

ENTITY = TypeVar('ENTITY', bound=Base)


class BaseRepository(Generic[ENTITY], metaclass=ABCMeta):
    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    @abstractmethod
    def _table(self) -> Type[ENTITY]:
        ...

    async def _execute_scalars(self, stmt: Executable) -> Result:
        result = await self._session.execute(stmt)
        return result.scalars()

    async def get_by_id(self, entity_id: int) -> Optional[ENTITY]:
        stmt = select(self._table).where(self._table.id == entity_id)
        result = await self._execute_scalars(stmt)
        return result.first()

    async def get_all(self) -> List[ENTITY]:
        stmt = select(self._table)
        result = await self._execute_scalars(stmt)
        return result.all()

    async def exists(self, entity_id: int) -> bool:
        stmt = select(self._table).where(self._table.id == entity_id)
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()

    async def add(self, entity: ENTITY) -> ENTITY:
        self._session.add(entity)

        Logger.log(entity, "Added")
        return entity

    async def add_all(self, entities: List[ENTITY]) -> List[ENTITY]:
        self._session.add_all(entities)

        Logger.log(type(entities[0]).__name__, f"Added {len(entities)} new entries")
        return entities

    async def remove(self, entity: ENTITY) -> ENTITY:
        await self._session.delete(entity)

        Logger.log(entity, "Removed")
        return entity

    async def remove_by_id(self, entity_id: int) -> Optional[ENTITY]:
        entity = await self.get_by_id(entity_id)
        stmt = delete(self._table).where(self._table.id == entity_id)
        await self._session.execute(stmt)

        Logger.log(entity_id, "Removed")
        return entity

    async def upsert(self, entity: ENTITY) -> ENTITY:
        if await self.exists(entity.id):
            return await self.update(entity)

        return await self.add(entity)

    async def update(self, entity: ENTITY) -> ENTITY:
        stmt = update(self._table) \
            .where(self._table.id == entity.id) \
            .values(Utils.get_class_fields(entity))

        await self._session.execute(stmt)

        Logger.log(entity, "Updated")
        return entity
