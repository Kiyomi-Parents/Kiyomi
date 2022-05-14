from typing import Optional, List, Type

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from src.kiyomi.database import BaseRepository
from src.log import Logger
from ..model.guild_player import GuildPlayer


class GuildPlayerRepository(BaseRepository[GuildPlayer]):

    @property
    def _table(self) -> Type[GuildPlayer]:
        return GuildPlayer

    async def get_all_by_guild_id(self, guild_id: int) -> List[GuildPlayer]:
        stmt = select(self._table).where(self._table.guild_id == guild_id)
        return await self._all(stmt)

    async def get_all_by_member_id(self, member_id: int) -> List[GuildPlayer]:
        stmt = select(self._table).where(self._table.member_id == member_id)
        return await self._all(stmt)

    async def get_by_guild_id_and_player_id(self, guild_id: int, player_id: str) -> Optional[GuildPlayer]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.player_id == player_id)
        return await self._first(stmt)

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildPlayer]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.member_id == member_id)
        return await self._first(stmt)

    async def get_by_guild_id_and_member_id_and_player_id(
            self,
            guild_id: int,
            member_id: int,
            player_id: str
    ) -> Optional[GuildPlayer]:
        stmt = select(self._table) \
            .where(self._table.guild_id == guild_id) \
            .where(self._table.member_id == member_id) \
            .where(self._table.player_id == player_id) \
            .options(
                joinedload(GuildPlayer.guild),
                joinedload(GuildPlayer.member),
                joinedload(GuildPlayer.player)
            )
        return await self._first(stmt)

    async def remove_by_guild_id_and_member_id_and_player_id(
            self,
            guild_id: int,
            member_id: int,
            player_id: str
    ) -> Optional[GuildPlayer]:
        entity = await self.get_by_guild_id_and_member_id_and_player_id(guild_id, member_id, player_id)
        stmt = delete(self._table).where(self._table.id == entity.id)
        await self._session.execute(stmt)

        Logger.log(entity, "Removed")
        return entity
