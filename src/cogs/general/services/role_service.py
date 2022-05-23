from typing import List, Optional

import discord
from discord import Colour, DiscordException

from src.cogs.security import Security
from src.kiyomi import Kiyomi
from .general_service import GeneralService
from .guild_service import GuildService
from .member_service import MemberService
from ..errors import GeneralCogException, RoleNotFound, FailedToCreateRole, FailedToDeleteRole, FailedToAddToUser, \
    FailedToRemoveFromUser
from ..storage import UnitOfWork
from ..storage.model.member_role import MemberRole
from ..storage.model.role import Role


class RoleService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService, member_service: MemberService):
        super().__init__(bot, uow)

        self.guild_service = guild_service
        self.member_service = member_service

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        before_role_ids = set([role.id for role in before.roles])
        after_role_ids = set([role.id for role in after.roles])

        diff_role_ids = before_role_ids - after_role_ids

        async with self.uow:
            for diff_role_id in diff_role_ids:
                member_role = await self.uow.member_roles.delete_by_guild_id_and_member_id_and_role_id(
                        after.guild.id,
                        after.id,
                        diff_role_id
                )

                if member_role is not None:
                    self.bot.events.emit("on_member_role_removed", member_role)

    async def on_role_delete(self, role: discord.role):
        async with self.uow:
            db_role = await self.uow.roles.remove_by_id(role.id)

            if db_role is not None:
                self.bot.events.emit("on_guild_role_removed", db_role)

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
            async with self.uow:
                await self.uow.roles.remove_by_id(role_id)

            raise RoleNotFound(guild_id, role_id)

        return discord_role

    @Security.can_edit_roles()
    async def create_role(self, guild_id: int, name: str, colour: Colour, hoist: bool, reason: str) -> Role:
        discord_guild = await self.guild_service.get_discord_guild(guild_id)

        try:
            role = await discord_guild.create_role(name=name, colour=colour, hoist=hoist, reason=reason)

            async with self.uow:
                return await self.uow.roles.add(Role(role.id, discord_guild.id, role.name))
        except DiscordException as error:
            raise FailedToCreateRole(guild_id, name, reason) from error

    @Security.can_edit_roles()
    async def delete_role(self, guild_id: int, role_id: int, reason: str) -> None:
        try:
            discord_role = await self.get_discord_role(guild_id, role_id)
        except RoleNotFound as error:
            async with self.uow:
                await self.uow.roles.remove_by_id(role_id)

            raise error

        try:
            await discord_role.delete(reason=reason)
        except DiscordException as error:
            raise FailedToDeleteRole(guild_id, role_id, reason) from error
        finally:
            async with self.uow:
                await self.uow.roles.remove_by_id(role_id)

    @Security.can_edit_roles()
    async def add_role_to_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> MemberRole:
        discord_member = await self.member_service.get_discord_member(guild_id, member_id)
        discord_role = await self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.add_roles(discord_role, reason=reason)

            async with self.uow:
                return await self.uow.member_roles.add(MemberRole(guild_id, member_id, role_id))
        except DiscordException as error:
            raise FailedToAddToUser(guild_id, member_id, role_id, reason) from error

    @Security.can_edit_roles()
    async def remove_role_from_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_member = await self.member_service.get_discord_member(guild_id, member_id)
        discord_role = await self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.remove_roles(discord_role, reason=reason)
        except (DiscordException, GeneralCogException):
            raise FailedToRemoveFromUser(guild_id, member_id, role_id, reason)
        finally:
            async with self.uow:
                await self.uow.member_roles.delete_by_guild_id_and_member_id_and_role_id(guild_id, member_id, role_id)

    async def get_member_role(self, guild_id: int, member_id: int, role_id: int) -> Optional[Role]:
        discord_member = await self.member_service.get_discord_member(guild_id, member_id)

        return discord_member.get_role(role_id)

    async def get_member_roles(self, guild_id: int, member_id: int) -> List[Role]:
        discord_member = await self.member_service.get_discord_member(guild_id, member_id)

        return discord_member.roles

    async def member_has_role(self, guild_id: int, member_id: int, role_id: int) -> bool:
        role = await self.get_member_role(guild_id, member_id, role_id)

        return role is not None
