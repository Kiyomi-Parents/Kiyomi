from abc import abstractmethod
from typing import Generic, TypeVar

from ..service.base_service_unit_of_work import BaseServiceUnitOfWork

TArg = TypeVar("TArg")
TReturn = TypeVar("TReturn")
TServiceUnitOfWork = TypeVar("TServiceUnitOfWork", bound=BaseServiceUnitOfWork)


class ErrorArgResolver(Generic[TServiceUnitOfWork, TArg, TReturn]):
    def __init__(self, service_uow: TServiceUnitOfWork):
        self.service_uow = service_uow

    @abstractmethod
    async def resolve_detailed(self, argument: TArg) -> TReturn:
        pass

    @abstractmethod
    async def resolve(self, argument: TArg) -> TReturn:
        pass

    @property
    @abstractmethod
    def arg_name(self) -> str:
        pass
