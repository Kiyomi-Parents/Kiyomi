from sqlalchemy.ext.asyncio import AsyncSession

from .repository.achievement_role_member_repository import AchievementRoleMemberRepository
from .repository.achievement_role_repository import AchievementRoleRepository
from src.kiyomi.database import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.achievement_roles = AchievementRoleRepository(session)
        self.achievement_role_members = AchievementRoleMemberRepository(session)
