from typing import Type, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable

from src.kiyomi.database import BaseRepository
from ..model.guild_twitch_streamer import GuildTwitchStreamer


class GuildTwitchStreamerRepository(BaseRepository[GuildTwitchStreamer]):

    # TODO: figure out what to do with orphan twitch_streamers

    def _eager_load_all(self, stmt: Executable):
        return stmt.options(
            selectinload(self._table.guild),
            selectinload(self._table.member),
            selectinload(self._table.twitch_streamer)
        )

    @property
    def _table(self) -> Type[GuildTwitchStreamer]:
        return GuildTwitchStreamer

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildTwitchStreamer]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.member_id == member_id)
        stmt = self._eager_load_all(stmt)
        return await self._first(stmt)

    async def get_all_by_member_id(self, member_id: int) -> List[GuildTwitchStreamer]:
        stmt = select(self._table).where(self._table.member_id == member_id)
        stmt = self._eager_load_all(stmt)
        return await self._all(stmt)

    async def get_all_by_twitch_streamer_id(self, twitch_streamer_id: str) -> List[GuildTwitchStreamer]:
        stmt = select(self._table).where(self._table.twitch_streamer_id == twitch_streamer_id)
        stmt = self._eager_load_all(stmt)
        return await self._all(stmt)
