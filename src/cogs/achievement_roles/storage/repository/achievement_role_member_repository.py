from typing import Optional, Type

from sqlalchemy import select

from src.kiyomi.database import BaseRepository
from ..model.achievement_role_member import AchievementRoleMember


class AchievementRoleMemberRepository(BaseRepository[AchievementRoleMember]):
    @property
    def _table(self) -> Type[AchievementRoleMember]:
        return AchievementRoleMember

    async def get_by_all(
            self,
            guild_id: int,
            member_id: int,
            achievement_role_id: int
    ) -> Optional[AchievementRoleMember]:
        stmt = select(self._table) \
            .where(self._table.guild_id == guild_id) \
            .where(self._table.member_id == member_id) \
            .where(self._table.achievement_role_id == achievement_role_id)
        return await self._first(stmt)
