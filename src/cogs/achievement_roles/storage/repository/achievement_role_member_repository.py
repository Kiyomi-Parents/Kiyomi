from typing import Optional, List

from sqlalchemy.orm import Query

from src.kiyomi.database import BaseRepository
from ..model.achievement_role_member import AchievementRoleMember


class AchievementRoleMemberRepository(BaseRepository[AchievementRoleMember]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(AchievementRoleMember) \
            .filter(AchievementRoleMember.id == entry_id)

    def get_all(self) -> Optional[List[AchievementRoleMember]]:
        return self.session.query(AchievementRoleMember) \
            .all()

    def get_by_all(self, guild_id: int, member_id: int, achievement_role_id: int) -> Optional[AchievementRoleMember]:
        return self.session.query(AchievementRoleMember) \
            .filter(AchievementRoleMember.guild_id == guild_id) \
            .filter(AchievementRoleMember.member_id == member_id) \
            .filter(AchievementRoleMember.achievement_role_id == achievement_role_id) \
            .first()
