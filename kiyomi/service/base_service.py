from typing import Generic, TypeVar, Dict, Optional, List, Any

from .base_basic_service import BaseBasicService
from ..database.database import Base
from ..database.base_storage_unit_of_work import BaseStorageUnitOfWork
from ..base_repository import BaseRepository
from kiyomi.kiyomi import Kiyomi

TEntity = TypeVar("TEntity", bound=Base)
TStorageUnitOfWork = TypeVar("TStorageUnitOfWork", bound=BaseStorageUnitOfWork)
TRepository = TypeVar("TRepository", bound=BaseRepository)


class BaseService(
    Generic[TEntity, TRepository, TStorageUnitOfWork], BaseBasicService[TStorageUnitOfWork], BaseRepository[TEntity]
):
    def __init__(self, bot: Kiyomi, repository: TRepository, storage_uow: TStorageUnitOfWork):
        super().__init__(bot, storage_uow)
        self.repository = repository

    async def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        return await self.repository.get_by_id(entity_id)

    async def get_all(self) -> List[TEntity]:
        return await self.repository.get_all()

    async def exists(self, entity_id: int) -> bool:
        return await self.repository.exists(entity_id)

    async def add(self, entity: TEntity) -> TEntity:
        return await self.repository.add(entity)

    async def add_all(self, entities: List[TEntity]) -> List[TEntity]:
        return await self.repository.add_all(entities)

    async def remove(self, entity: TEntity) -> TEntity:
        return await self.repository.remove(entity)

    async def remove_by_id(self, entity_id: int) -> Optional[TEntity]:
        return await self.repository.remove_by_id(entity_id)

    async def upsert(self, entity: TEntity) -> TEntity:
        return await self.repository.upsert(entity)

    async def update(self, entity_id: int, values: Dict[str, Any]) -> TEntity:
        return await self.repository.update(entity_id, values)

    async def update_entity(self, entity: TEntity) -> TEntity:
        return await self.repository.update_entity(entity)
