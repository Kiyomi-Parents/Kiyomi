from typing import Generic, TypeVar

from .database import BaseUnitOfWork
from .kiyomi import Kiyomi

T = TypeVar("T", bound=BaseUnitOfWork)


class BaseService(Generic[T]):
    def __init__(self, bot: Kiyomi, uow: T):
        self.bot = bot
        self.uow = uow
