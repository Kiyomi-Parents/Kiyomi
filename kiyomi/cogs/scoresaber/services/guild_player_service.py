from typing import Optional, List

from ..storage import StorageUnitOfWork
from ..storage.model.guild_player import GuildPlayer
from ..storage.repository.guild_player_repository import GuildPlayerRepository
from kiyomi import BaseService


class GuildPlayerService(BaseService[GuildPlayer, GuildPlayerRepository, StorageUnitOfWork]):
    async def get_all_by_guild_id(self, guild_id: int) -> List[GuildPlayer]:
        return await self.repository.get_all_by_guild_id(guild_id)

    async def get_all_by_member_id(self, member_id: int) -> List[GuildPlayer]:
        return await self.repository.get_all_by_member_id(member_id)

    async def get_by_guild_id_and_player_id(self, guild_id: int, player_id: str) -> Optional[GuildPlayer]:
        return await self.repository.get_by_guild_id_and_player_id(guild_id, player_id)

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildPlayer]:
        return await self.repository.get_by_guild_id_and_member_id(guild_id, member_id)

    async def get_by_guild_id_and_member_id_and_player_id(
            self, guild_id: int, member_id: int, player_id: str
    ) -> Optional[GuildPlayer]:
        return await self.repository.get_by_guild_id_and_member_id_and_player_id(guild_id, member_id, player_id)

    async def remove_by_guild_id_and_member_id_and_player_id(
            self, guild_id: int, member_id: int, player_id: str
    ) -> Optional[GuildPlayer]:
        return await self.repository.remove_by_guild_id_and_member_id_and_player_id(guild_id, member_id, player_id)
