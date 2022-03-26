from src.kiyomi import Kiyomi, BaseService
from ..storage import UnitOfWork


class AchievementRolesService(BaseService[UnitOfWork]):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)
