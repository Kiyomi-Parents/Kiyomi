from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Optional, List, Dict

from .database import Base

TEntity = TypeVar("TEntity", bound=Base)


class BaseRepository(Generic[TEntity], metaclass=ABCMeta):
    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TEntity]:
        pass

    @abstractmethod
    async def exists(self, entity_id: int) -> bool:
        pass

    @abstractmethod
    async def add(self, entity: TEntity) -> TEntity:
        pass

    @abstractmethod
    async def add_all(self, entities: List[TEntity]) -> List[TEntity]:
        pass

    @abstractmethod
    async def remove(self, entity: TEntity) -> TEntity:
        pass

    @abstractmethod
    async def remove_by_id(self, entity_id: int) -> Optional[TEntity]:
        pass

    @abstractmethod
    async def upsert(self, entity: TEntity) -> TEntity:
        pass

    @abstractmethod
    async def update(self, entity_id: int, values: Dict[str, any]) -> TEntity:
        pass

    @abstractmethod
    async def update_entity(self, entity: TEntity) -> TEntity:
        pass
