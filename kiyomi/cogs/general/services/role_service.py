from typing import List, Optional

import discord
from discord import Colour, DiscordException

from kiyomi.cogs.security import Security
from kiyomi import BaseService
from ..errors import (
    GeneralCogException,
    RoleNotFound,
    FailedToCreateRole,
    FailedToDeleteRole,
    FailedToAddToUser,
    FailedToRemoveFromUser,
)
from ..storage import StorageUnitOfWork
from ..storage.model.member_role import MemberRole
from ..storage.model.role import Role
from ..storage.repository.role_repository import RoleRepository


class RoleService(BaseService[Role, RoleRepository, StorageUnitOfWork]):
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        before_role_ids = set([role.id for role in before.roles])
        after_role_ids = set([role.id for role in after.roles])

        diff_role_ids = before_role_ids - after_role_ids

        for diff_role_id in diff_role_ids:
            member_role = await self.storage_uow.member_roles.delete_by_guild_id_and_member_id_and_role_id(
                after.guild.id, after.id, diff_role_id
            )

            if member_role is not None:
                self.bot.events.emit("on_member_role_removed", member_role)

    async def on_role_delete(self, role: discord.role):
        db_role = await self.repository.remove_by_id(role.id)

        if db_role is not None:
            self.bot.events.emit("on_guild_role_removed", db_role)

    async def get_discord_role(self, discord_guild: discord.Guild, role_id: int) -> discord.Role:
        discord_role = discord_guild.get_role(role_id)

        if discord_role is None:
            tmp_discord_roles = await discord_guild.fetch_roles()

            for tmp_discord_role in tmp_discord_roles:
                if tmp_discord_role.id == role_id:
                    discord_role = tmp_discord_role
                    break

        if discord_role is None:
            await self.repository.remove_by_id(role_id)
            raise RoleNotFound(discord_guild.id, role_id)

        return discord_role

    @Security.can_edit_roles()
    async def create_role(self, discord_guild: discord.Guild, name: str, colour: Colour, hoist: bool, reason: str) -> Role:
        try:
            role = await discord_guild.create_role(name=name, colour=colour, hoist=hoist, reason=reason)

            return await self.repository.add(Role(role.id, discord_guild.id, role.name))
        except DiscordException as error:
            raise FailedToCreateRole(discord_guild.id, name, reason) from error

    @Security.can_edit_roles()
    async def delete_role(self, discord_guild: discord.Guild, role_id: int, reason: str) -> None:
        try:
            discord_role = await self.get_discord_role(discord_guild, role_id)
        except RoleNotFound as error:
            await self.repository.remove_by_id(role_id)

            raise error

        try:
            await discord_role.delete(reason=reason)
        except DiscordException as error:
            raise FailedToDeleteRole(discord_guild.id, role_id, reason) from error
        finally:
            await self.repository.remove_by_id(role_id)

    @Security.can_edit_roles()
    async def add_role_to_member(
        self, discord_member: discord.Member, discord_role: discord.Role, reason: str
    ) -> MemberRole:
        try:
            await discord_member.add_roles(discord_role, reason=reason)

            return await self.storage_uow.member_roles.add(
                MemberRole(discord_member.guild.id, discord_member.id, discord_role.id)
            )
        except DiscordException as error:
            raise FailedToAddToUser(discord_member.guild.id, discord_member.id, discord_role.id, reason) from error

    @Security.can_edit_roles()
    async def remove_role_from_member(self, discord_member: discord.Member, discord_role: discord.Role, reason: str) -> None:
        try:
            await discord_member.remove_roles(discord_role, reason=reason)
        except (DiscordException, GeneralCogException):
            raise FailedToRemoveFromUser(discord_member.guild.id, discord_member.id, discord_role.id, reason)
        finally:
            await self.storage_uow.member_roles.delete_by_guild_id_and_member_id_and_role_id(
                discord_member.guild.id, discord_member.id, discord_role.id
            )

    async def get_member_role(self, discord_member: discord.Member, role_id: int) -> Optional[Role]:
        return discord_member.get_role(role_id)

    async def get_member_roles(self, discord_member: discord.Member) -> List[Role]:
        return discord_member.roles

    async def member_has_role(self, discord_member: discord.Member, role_id: int) -> bool:
        role = await self.get_member_role(discord_member, role_id)

        return role is not None
