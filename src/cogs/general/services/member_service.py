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
                guild_member = self.uow.guild_members.get_by_guild_id_and_member_id(guild_id, member_id)

                if guild_member is not None:
                    self.uow.guild_members.remove(guild_member)

                raise MemberNotFoundException(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        if discord_member is None:
            raise MemberNotFoundException(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        return discord_member

    def register_member(self, discord_member: discord.Member):
        member = self.uow.members.get_by_id(discord_member.id)

        if member is None:
            self.uow.members.add(Member(discord_member.id, discord_member.name))
        else:
            if member.name != discord_member.name:
                self.uow.members.update(Member(member.id, discord_member.name))
                self.uow.save_changes()  # TODO: Figure out if this is a good place for this

    def register_guild_member(self, discord_member: discord.Member):
        guild_member = self.uow.guild_members.get_by_guild_id_and_member_id(discord_member.guild.id, discord_member.id)

        if guild_member is None:
            self.uow.members.add(GuildMember(discord_member.guild.id, discord_member.id))
