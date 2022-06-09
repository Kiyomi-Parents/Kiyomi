from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Optional, List, Type, Dict

from sqlalchemy import select, exists, delete, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Executable

from src.log import Logger
from .database import Base
from ..utils import Utils

ENTITY = TypeVar("ENTITY", bound=Base)


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

    async def _first(self, stmt: Executable) -> Optional[ENTITY]:
        result = await self._execute_scalars(stmt)
        return result.first()

    async def _all(self, stmt: Executable) -> List[ENTITY]:
        result = await self._execute_scalars(stmt)
        return result.unique().all()

    async def get_by_id(self, entity_id: int) -> Optional[ENTITY]:
        stmt = select(self._table).where(self._table.id == entity_id) \
            .options(joinedload('*'))
        return await self._first(stmt)

    async def get_all(self) -> List[ENTITY]:
        stmt = select(self._table).options(joinedload("*"))
        return await self._all(stmt)

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

        Logger.log(entity, "Removed")
        return entity

    async def upsert(self, entity: ENTITY) -> ENTITY:
        if await self.exists(entity.id):
            return await self.update_entity(entity)

        return await self.add(entity)

    async def update(self, entity_id: int, values: Dict[str, any]) -> ENTITY:
        entity = await self.get_by_id(entity_id)
        stmt = update(self._table).where(self._table.id == entity_id).values(values)

        await self._session.execute(stmt)

        Logger.log(entity, "Updated")
        return entity

    async def update_entity(self, entity: ENTITY) -> ENTITY:
        return await self.update(entity.id, Utils.get_class_fields(entity))
