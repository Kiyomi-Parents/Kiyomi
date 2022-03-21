from ..storage import UnitOfWork
from src.kiyomi import BaseService, Kiyomi


class GeneralService(BaseService[UnitOfWork]):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)
