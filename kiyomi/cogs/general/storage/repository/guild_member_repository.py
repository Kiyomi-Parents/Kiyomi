from typing import Optional, List, Type

from sqlalchemy import select, delete

from ..model.guild_member import GuildMember
from kiyomi.database import BaseStorageRepository


class GuildMemberRepository(BaseStorageRepository[GuildMember]):
    @property
    def _table(self) -> Type[GuildMember]:
        return GuildMember

    async def get_all_by_guild_id(self, guild_id: int) -> List[GuildMember]:
        stmt = select(self._table).where(self._table.guild_id == guild_id)
        result = await self._execute_scalars(stmt)
        return result.all()

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildMember]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.member_id == member_id)
        result = await self._execute_scalars(stmt)
        return result.first()

    async def delete_by_guild_id_and_member_id(self, guild_id: int, member_id: int):
        stmt = delete(self._table).where(self._table.guild_id == guild_id).where(self._table.member_id == member_id)
        await self._session.execute(stmt)
