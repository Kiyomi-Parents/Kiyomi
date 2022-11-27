from sqlalchemy.ext.asyncio import AsyncSession

from .repository.achievement_role_member_repository import (
    AchievementRoleMemberRepository,
)
from .repository.achievement_role_repository import AchievementRoleRepository
from kiyomi.database import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.achievement_roles = AchievementRoleRepository(self._session)
        self.achievement_role_members = AchievementRoleMemberRepository(self._session)
