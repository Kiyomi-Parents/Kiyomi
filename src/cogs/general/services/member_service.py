import discord
from discord import NotFound

from src.kiyomi import Kiyomi
from .general_service import GeneralService
from .guild_service import GuildService
from ..errors import MemberNotFoundException
from ..storage import UnitOfWork
from ..storage.model.guild_member import GuildMember
from ..storage.model.member import Member


class MemberService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService):
        super().__init__(bot, uow)

        self.guild_service = guild_service

    async def get_discord_member(self, guild_id: int, member_id: int) -> discord.Member:
        discord_guild = await self.guild_service.get_discord_guild(guild_id)
        discord_member = discord_guild.get_member(member_id)

        if discord_member is None:
            try:
                discord_member = await discord_guild.fetch_member(member_id)
            except NotFound:
                await self.uow.guild_members.delete_by_guild_id_and_member_id(guild_id, member_id)

                raise MemberNotFoundException(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        if discord_member is None:
            raise MemberNotFoundException(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        return discord_member

    async def register_member(self, guild_id: int, member_id: int) -> Member:
        async with self.uow:
            discord_member = await self.get_discord_member(guild_id, member_id)
            return await self.uow.members.upsert(Member(discord_member.id, discord_member.name))

    async def unregister_member(self, member_id: int):
        async with self.uow:
            return await self.uow.members.remove_by_id(member_id)

    async def register_guild_member(self, guild_id: int, member_id: int) -> GuildMember:
        async with self.uow:
            await self.guild_service.register_guild(guild_id)

            guild_member = await self.uow.guild_members.get_by_guild_id_and_member_id(guild_id, member_id)

            if guild_member is None:
                return await self.uow.members.add(GuildMember(guild_id, member_id))

    async def unregister_guild_member(self, guild_id: int, member_id: int):
        async with self.uow:
            await self.uow.guild_members.delete_by_guild_id_and_member_id(guild_id, member_id)
