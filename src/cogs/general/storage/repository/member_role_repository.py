from typing import Optional, Type

from sqlalchemy import select, delete

from ..model.member_role import MemberRole
from src.kiyomi.database import BaseRepository


class MemberRoleRepository(BaseRepository[MemberRole]):
    @property
    def _table(self) -> Type[MemberRole]:
        return MemberRole

    async def get_by_guild_id_and_member_id_and_role_id(
        self, guild_id: int, member_id: int, role_id: int
    ) -> Optional[MemberRole]:
        stmt = (
            select(self._table)
            .where(self._table.guild_id == guild_id)
            .where(self._table.member_id == member_id)
            .where(self._table.role_id == role_id)
        )
        result = await self._execute_scalars(stmt)
        return result.first()

    async def delete_by_guild_id_and_member_id_and_role_id(
        self, guild_id: int, member_id: int, role_id: int
    ) -> Optional[MemberRole]:
        entity = await self.get_by_guild_id_and_member_id_and_role_id(guild_id, member_id, role_id)
        stmt = (
            delete(self._table)
            .where(self._table.guild_id == guild_id)
            .where(self._table.member_id == member_id)
            .where(self._table.role_id == role_id)
        )
        await self._session.execute(stmt)
        return entity
