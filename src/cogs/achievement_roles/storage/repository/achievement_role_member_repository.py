from typing import Optional, List

from src.database import Repository
from ..model.achievement_role_member import AchievementRoleMember


class AchievementRoleMemberRepository(Repository[AchievementRoleMember]):
    def get_by_id(self, entry_id: int) -> Optional[AchievementRoleMember]:
        return self._db.session.query(AchievementRoleMember) \
            .filter(AchievementRoleMember.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[AchievementRoleMember]]:
        return self._db.session.query(AchievementRoleMember) \
            .all()

    def get_by_all(self, guild_id: int, member_id: int, achievement_role_id: int) -> Optional[AchievementRoleMember]:
        return self._db.session.query(AchievementRoleMember) \
            .filter(AchievementRoleMember.guild_id == guild_id) \
            .filter(AchievementRoleMember.member_id == member_id) \
            .filter(AchievementRoleMember.achievement_role_id == achievement_role_id) \
            .first()
