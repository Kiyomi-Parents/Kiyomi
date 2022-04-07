import discord
from discord import Colour, DiscordException

from src.cogs.security import Security
from src.kiyomi import Kiyomi
from src.log import Logger
from .general_service import GeneralService
from .guild_service import GuildService
from .member_service import MemberService
from ..errors import RoleNotFoundException
from ..storage import UnitOfWork
from ..storage.model.member_role import MemberRole
from ..storage.model.role import Role


class RoleService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService, member_service: MemberService):
        super().__init__(bot, uow)

        self.guild_service = guild_service
        self.member_service = member_service

    async def get_discord_role(self, guild_id: int, role_id: int) -> discord.Role:
        discord_guild = await self.guild_service.get_discord_guild(guild_id)
        discord_role = discord_guild.get_role(role_id)

        if discord_role is None:
            tmp_discord_roles = await discord_guild.fetch_roles()

            for tmp_discord_role in tmp_discord_roles:
                if tmp_discord_role.id == role_id:
                    discord_role = tmp_discord_role
                    break

        if discord_role is None:
            raise RoleNotFoundException(f"Could not find role with id {role_id} in guild {discord_guild.name}")

        return discord_role

    @Security.can_edit_roles()
    async def create_role(self, guild_id: int, name: str, colour: Colour, hoist: bool, reason: str) -> Role:
        discord_guild = await self.guild_service.get_discord_guild(guild_id)

        try:
            role = await discord_guild.create_role(name=name, colour=colour, hoist=hoist, reason=reason)
            return self.uow.roles.add(Role(role.id, discord_guild.id, role.name))
        except DiscordException as error:
            Logger.log(discord_guild.name, f"Failed to add role: {name}")
            raise error

    @Security.can_edit_roles()
    async def delete_role(self, guild_id: int, role_id: int, reason: str) -> None:
        try:
            discord_role = await self.get_discord_role(guild_id, role_id)
        except RoleNotFoundException as error:
            role = self.uow.roles.get_by_id(role_id)

            if role is not None:
                self.uow.roles.remove(role)

            raise error

        try:
            await discord_role.delete(reason=reason)
        except DiscordException as error:
            Logger.log(guild_id, f"Failed to remove role: {discord_role.name} ({discord_role.id})")
            raise error
        finally:
            role = self.uow.roles.get_by_id(role_id)

            if role is not None:
                self.uow.roles.remove(role)

    @Security.can_edit_roles()
    async def add_role_to_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_member = await self.member_service.get_discord_member(guild_id, member_id)
        discord_role = await self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.add_roles(discord_role, reason=reason)
            self.uow.member_roles.add(MemberRole(guild_id, member_id, role_id))
        except DiscordException as error:
            Logger.log(guild_id, f"Failed to add role {discord_role.name} ({discord_role.id}) to member {discord_member.name} ({discord_member.id})")
            raise error

    @Security.can_edit_roles()
    async def remove_role_from_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_member = await self.member_service.get_discord_member(guild_id, member_id)
        discord_role = await self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.remove_roles(discord_role, reason=reason)

            role = self.uow.member_roles.get_by_guild_id_and_member_id_and_role_id(guild_id, member_id, role_id)

            if role is not None:
                self.uow.member_roles.remove(role)

        except DiscordException as error:
            Logger.log(guild_id, f"Failed to add role {discord_role.name} ({discord_role.id}) to member {discord_member.name} ({discord_member.id})")
            raise error
