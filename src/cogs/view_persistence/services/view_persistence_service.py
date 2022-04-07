from ..storage.unit_of_work import UnitOfWork
from src.kiyomi import BaseService, Kiyomi


class ViewPersistenceService(BaseService[UnitOfWork]):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)
