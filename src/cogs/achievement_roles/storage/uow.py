from sqlalchemy.orm import Session

from .repository.achievement_role_member_repository import AchievementRoleMemberRepository
from .repository.achievement_role_repository import AchievementRoleRepository
from src.kiyomi.database import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.achievement_role_repo = AchievementRoleRepository(session)
        self.achievement_role_member_repo = AchievementRoleMemberRepository(session)
