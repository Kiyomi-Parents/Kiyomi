from typing import Optional, List, Type

from sqlalchemy import select

from src.kiyomi.database import BaseRepository
from ..model.achievement_role import AchievementRole


class AchievementRoleRepository(BaseRepository[AchievementRole]):
    @property
    def _table(self) -> Type[AchievementRole]:
        return AchievementRole

    async def get_all_by_guild_id_and_group(self, guild_id: int, group: str) -> List[AchievementRole]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.group == group)
        return await self._all(stmt)

    async def get_by_guild_id_and_group_and_identifier(
        self, guild_id: int, group: str, identifier: str
    ) -> Optional[AchievementRole]:
        stmt = (
            select(self._table)
            .where(self._table.guild_id == guild_id)
            .where(self._table.group == group)
            .where(self._table.identifier == identifier)
        )
        return await self._first(stmt)
