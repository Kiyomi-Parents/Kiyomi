from typing import Generic, TypeVar

from kiyomi.kiyomi import Kiyomi
from ..database.base_storage_unit_of_work import BaseStorageUnitOfWork

TStorageUnitOfWork = TypeVar("TStorageUnitOfWork", bound=BaseStorageUnitOfWork)


class BaseBasicService(Generic[TStorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: TStorageUnitOfWork):
        self.bot = bot
        self.storage_uow = storage_uow
