from sqlalchemy.orm import Session

from src.database import BaseUnitOfWork
from .repository import AchievementRoleRepository, AchievementRoleMemberRepository


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.achievement_role_repo = AchievementRoleRepository(session)
        self.achievement_role_member_repo = AchievementRoleMemberRepository(session)
