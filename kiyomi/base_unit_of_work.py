from abc import abstractmethod, ABCMeta
from typing import TypeVar

TEntity = TypeVar("TEntity")


class BaseUnitOfWork(metaclass=ABCMeta):
    @abstractmethod
    async def refresh(self, entry: TEntity) -> TEntity:
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def save_changes(self):
        pass
