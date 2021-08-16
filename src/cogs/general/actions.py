import discord
from discord import Colour, DiscordException
from discord.ext.commands import MemberNotFound

from .errors import GuildNotFoundException, RoleNotFoundException
from .storage.model import Member, GuildMember, Guild, Role, MemberRole
from .storage.uow import UnitOfWork
from ..security import Security
from ...log import Logger


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_discord_guild(self, guild_id: int) -> discord.Guild:
        discord_guild = self.uow.bot.get_guild(guild_id)

        if discord_guild is None:
            raise GuildNotFoundException(f"Could not find guild with id {guild_id}")

        return discord_guild

    async def get_discord_member(self, guild_id: int, member_id: int) -> discord.Member:
        discord_guild = self.get_discord_guild(guild_id)
        discord_member = await discord_guild.fetch_member(member_id)

        if discord_member is None:
            raise MemberNotFound(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        return discord_member

    def get_discord_role(self, guild_id: int, role_id: int) -> discord.Role:
        discord_guild = self.get_discord_guild(guild_id)
        discord_role = discord_guild.get_role(role_id)

        if discord_role is None:
            raise RoleNotFoundException(f"Could not find role with id {role_id} in guild {discord_guild.name}")

        return discord_role

    def register_member(self, discord_member: discord.Member):
        member = self.uow.member_repo.get_by_id(discord_member.id)

        if member is None:
            self.uow.member_repo.add(Member(discord_member.id, discord_member.name))
        else:
            if member.name != discord_member.name:
                self.uow.member_repo.update(Member(member.id, discord_member.name))

    def register_guild_member(self, discord_member: discord.Member):
        guild_member = self.uow.guild_member_repo.get_by_guild_id_and_member_id(discord_member.guild.id, discord_member.id)

        if guild_member is None:
            self.uow.member_repo.add(GuildMember(discord_member.guild.id, discord_member.id))

    def register_guild(self, discord_guild: discord.Guild):
        guild = self.uow.guild_repo.get_by_id(discord_guild.id)

        if guild is None:
            self.uow.guild_repo.add(Guild(discord_guild.id, discord_guild.name))

    @Security.can_edit_roles()
    async def create_role(self, guild_id: int, name: str, colour: Colour, hoist: bool, reason: str) -> Role:
        discord_guild = self.get_discord_guild(guild_id)

        try:
            role = await discord_guild.create_role(name=name, colour=colour, hoist=hoist, reason=reason)
            return self.uow.role_repo.add(Role(role.id, discord_guild.id, role.name))
        except DiscordException as error:
            Logger.log(discord_guild.name, f"Failed to add role: {name}")
            raise error

    @Security.can_edit_roles()
    async def delete_role(self, guild_id: int, role_id: int, reason: str) -> None:
        try:
            discord_role = self.get_discord_role(guild_id, role_id)
        except RoleNotFoundException as error:
            role = self.uow.role_repo.get_by_id(role_id)

            if role is not None:
                self.uow.role_repo.remove(role)

            raise error

        try:
            await discord_role.delete(reason=reason)
        except DiscordException as error:
            Logger.log(guild_id, f"Failed to remove role: {discord_role.name} ({discord_role.id})")
            raise error
        finally:
            role = self.uow.role_repo.get_by_id(role_id)

            if role is not None:
                self.uow.role_repo.remove(role)

    @Security.can_edit_roles()
    async def add_role_to_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_member = await self.get_discord_member(guild_id, member_id)
        discord_role = self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.add_roles(discord_role, reason=reason)
            self.uow.member_role_repo.add(MemberRole(guild_id, member_id, role_id))
        except DiscordException as error:
            Logger.log(guild_id, f"Failed to add role {discord_role.name} ({discord_role.id}) to member {discord_member.name} ({discord_member.id})")
            raise error

    @Security.can_edit_roles()
    async def remove_role_from_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_member = await self.get_discord_member(guild_id, member_id)
        discord_role = self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.remove_roles(discord_role, reason=reason)

            role = self.uow.member_role_repo.get_by_guild_id_and_member_id_and_role_id(guild_id, member_id, role_id)

            if role is not None:
                self.uow.member_role_repo.remove(role)

        except DiscordException as error:
            Logger.log(guild_id, f"Failed to add role {discord_role.name} ({discord_role.id}) to member {discord_member.name} ({discord_member.id})")
            raise error
