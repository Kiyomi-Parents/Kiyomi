from typing import Generic, TypeVar

from src.database.base_unit_of_work import BaseUnitOfWork
from src.kiyomi import Kiyomi

T = TypeVar('T', bound=BaseUnitOfWork)


class BaseService(Generic[T]):
    def __init__(self, bot: Kiyomi, uow: T):
        self.bot = bot
        self.uow = uow
