from kiyomi.service.base_service_unit_of_work import BaseServiceUnitOfWork

from kiyomi import Kiyomi
from .achievement_role_member_service import AchievementRoleMemberService
from ..storage.storage_unit_of_work import StorageUnitOfWork


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.memberAchievementRoles = AchievementRoleMemberService(bot, storage_uow.achievement_role_members, storage_uow)
