from typing import Generic, TypeVar

from .service import BaseServiceUnitOfWork
from .kiyomi import Kiyomi

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)


class BaseTasks(Generic[TServiceUOW]):
    def __init__(self, bot: Kiyomi, service_uow: TServiceUOW):
        self.bot = bot
        self.service_uow = service_uow
