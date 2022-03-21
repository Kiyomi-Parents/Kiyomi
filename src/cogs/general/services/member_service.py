import discord
from discord.ext.commands import MemberNotFound

from src.kiyomi import Kiyomi
from .general_service import GeneralService
from .guild_service import GuildService
from ..storage import UnitOfWork, Member, GuildMember


class MemberService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService):
        super().__init__(bot, uow)

        self.guild_service = guild_service

    async def get_discord_member(self, guild_id: int, member_id: int) -> discord.Member:
        discord_guild = await self.guild_service.get_discord_guild(guild_id)
        discord_member = discord_guild.get_member(member_id)

        if discord_member is None:
            discord_member = await discord_guild.fetch_member(member_id)

        if discord_member is None:
            raise MemberNotFound(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        return discord_member

    def register_member(self, discord_member: discord.Member):
        member = self.uow.member_repo.get_by_id(discord_member.id)

        if member is None:
            self.uow.member_repo.add(Member(discord_member.id, discord_member.name))
        else:
            if member.name != discord_member.name:
                self.uow.member_repo.update(Member(member.id, discord_member.name))
                self.uow.save_changes()  # TODO: Figure out if this is a good place for this

    def register_guild_member(self, discord_member: discord.Member):
        guild_member = self.uow.guild_member_repo.get_by_guild_id_and_member_id(discord_member.guild.id, discord_member.id)

        if guild_member is None:
            self.uow.member_repo.add(GuildMember(discord_member.guild.id, discord_member.id))
