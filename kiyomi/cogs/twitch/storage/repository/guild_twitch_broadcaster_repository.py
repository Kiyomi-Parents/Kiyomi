import logging
from typing import Type, List, Optional

from sqlalchemy import select, delete

from kiyomi.database import BaseStorageRepository
from ..model.guild_twitch_broadcaster import GuildTwitchBroadcaster

_logger = logging.getLogger(__name__)


class GuildTwitchBroadcasterRepository(BaseStorageRepository[GuildTwitchBroadcaster]):
    @property
    def _table(self) -> Type[GuildTwitchBroadcaster]:
        return GuildTwitchBroadcaster

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildTwitchBroadcaster]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.member_id == member_id)
        return await self._first(stmt)

    async def get_all_by_member_id(self, member_id: int) -> List[GuildTwitchBroadcaster]:
        stmt = select(self._table).where(self._table.member_id == member_id)
        return await self._all(stmt)

    async def get_all_by_broadcaster_id(self, broadcaster_id: str) -> List[GuildTwitchBroadcaster]:
        stmt = select(self._table).where(self._table.twitch_broadcaster_id == broadcaster_id)
        return await self._all(stmt)

    async def delete_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildTwitchBroadcaster]:
        entity = await self.get_by_guild_id_and_member_id(guild_id, member_id)
        stmt = delete(self._table).where(self._table.id == entity.id)
        await self._session.execute(stmt)

        _logger.info(entity, "Removed")
        return entity
