from src.kiyomi import BaseService, Kiyomi
from ..storage import UnitOfWork


class GeneralService(BaseService[UnitOfWork]):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)
