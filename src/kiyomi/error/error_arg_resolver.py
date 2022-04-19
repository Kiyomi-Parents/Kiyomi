from abc import abstractmethod
from typing import Generic, TypeVar

TArg = TypeVar("TArg")
TReturn = TypeVar("TReturn")


class ErrorArgResolver(Generic[TArg, TReturn]):
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
