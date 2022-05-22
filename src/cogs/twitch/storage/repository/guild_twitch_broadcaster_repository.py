from typing import Type, List, Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable

from src.kiyomi.database import BaseRepository
from src.log import Logger
from ..model.guild_twitch_broadcaster import GuildTwitchBroadcaster


class GuildTwitchBroadcasterRepository(BaseRepository[GuildTwitchBroadcaster]):

    # TODO: figure out what to do with orphan twitch_broadcasters

    def _eager_load_all(self, stmt: Executable):
        return stmt.options(
            selectinload(self._table.guild),
            selectinload(self._table.member),
            selectinload(self._table.twitch_broadcaster)
        )

    @property
    def _table(self) -> Type[GuildTwitchBroadcaster]:
        return GuildTwitchBroadcaster

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildTwitchBroadcaster]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.member_id == member_id)
        stmt = self._eager_load_all(stmt)
        return await self._first(stmt)

    async def get_all_by_member_id(self, member_id: int) -> List[GuildTwitchBroadcaster]:
        stmt = select(self._table).where(self._table.member_id == member_id)
        stmt = self._eager_load_all(stmt)
        return await self._all(stmt)

    async def get_all_by_broadcaster_id(self, broadcaster_id: str) -> List[GuildTwitchBroadcaster]:
        stmt = select(self._table).where(self._table.twitch_broadcaster_id == broadcaster_id)
        stmt = self._eager_load_all(stmt)
        return await self._all(stmt)

    async def remove_by_guild_id_and_member_id(
            self,
            guild_id: int,
            member_id: int
    ) -> Optional[GuildTwitchBroadcaster]:
        entity = await self.get_by_guild_id_and_member_id(guild_id, member_id)
        stmt = delete(self._table).where(self._table.id == entity.id)
        await self._session.execute(stmt)

        Logger.log(entity, "Removed")
        return entity
