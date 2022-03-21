from typing import Optional, List

from sqlalchemy.orm import Query

from src.database import BaseRepository
from ..model.achievement_role import AchievementRole


class AchievementRoleRepository(BaseRepository[AchievementRole]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(AchievementRole) \
            .filter(AchievementRole.id == entry_id)

    def get_all(self) -> Optional[List[AchievementRole]]:
        return self.session.query(AchievementRole) \
            .all()

    def get_all_by_guild_id_and_group(self, guild_id: int, group: str) -> Optional[List[AchievementRole]]:
        return self.session.query(AchievementRole) \
            .filter(AchievementRole.guild_id == guild_id) \
            .filter(AchievementRole.group == group) \
            .all()

    def get_by_guild_id_and_group_and_identifier(self, guild_id: int, group: str, identifier: str) -> Optional[AchievementRole]:
        return self.session.query(AchievementRole) \
            .filter(AchievementRole.guild_id == guild_id) \
            .filter(AchievementRole.group == group) \
            .filter(AchievementRole.identifier == identifier) \
            .first()
