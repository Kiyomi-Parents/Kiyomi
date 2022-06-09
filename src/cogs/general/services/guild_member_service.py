from typing import List, Optional

from ..storage import StorageUnitOfWork
from ..storage.model.guild_member import GuildMember
from ..storage.repository.guild_member_repository import GuildMemberRepository
from src.kiyomi import BaseService


class GuildMemberService(BaseService[GuildMember, GuildMemberRepository, StorageUnitOfWork]):
    async def get_all_by_guild_id(self, guild_id: int) -> List[GuildMember]:
        return await self.repository.get_all_by_guild_id(guild_id)

    async def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildMember]:
        return await self.repository.get_by_guild_id_and_member_id(guild_id, member_id)

    async def delete_by_guild_id_and_member_id(self, guild_id: int, member_id: int):
        return await self.repository.delete_by_guild_id_and_member_id(guild_id, member_id)
