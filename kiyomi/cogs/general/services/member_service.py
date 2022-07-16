import discord
from discord import NotFound

from kiyomi import BaseService
from ..errors import MemberNotFoundException
from ..storage import StorageUnitOfWork
from ..storage.model.guild_member import GuildMember
from ..storage.model.member import Member
from ..storage.repository.member_repository import MemberRepository


class MemberService(BaseService[Member, MemberRepository, StorageUnitOfWork]):
    async def get_discord_member(self, discord_guild: discord.Guild, member_id: int) -> discord.Member:
        discord_member = discord_guild.get_member(member_id)

        if discord_member is None:
            try:
                discord_member = await discord_guild.fetch_member(member_id)
            except NotFound:
                await self.storage_uow.guild_members.delete_by_guild_id_and_member_id(discord_guild.id, member_id)

                raise MemberNotFoundException(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        if discord_member is None:
            raise MemberNotFoundException(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        return discord_member

    async def register_member(self, discord_guild: discord.Guild, member_id: int) -> Member:
        discord_member = await self.get_discord_member(discord_guild, member_id)

        return await self.repository.upsert(Member(discord_member.id, discord_member.name))

    async def unregister_member(self, member_id: int):
        return await self.repository.remove_by_id(member_id)

    async def register_guild_member(self, guild_id: int, member_id: int) -> GuildMember:
        guild_member = await self.storage_uow.guild_members.get_by_guild_id_and_member_id(guild_id, member_id)

        if guild_member is None:
            return await self.repository.add(GuildMember(guild_id, member_id))

    async def unregister_guild_member(self, guild_id: int, member_id: int):
        await self.storage_uow.guild_members.delete_by_guild_id_and_member_id(guild_id, member_id)

    async def upsert_member(self, discord_guild: discord.Guild, member_id: int) -> discord.Member:
        discord_member = await self.get_discord_member(discord_guild, member_id)
        await self.repository.upsert(Member(discord_member.id, discord_member.name))

        return discord_member
