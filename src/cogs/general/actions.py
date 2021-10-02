import random
import re
from typing import Optional

import discord
from discord import Colour, DiscordException
from discord.ext.commands import MemberNotFound

from .errors import GuildNotFoundException, RoleNotFoundException, EmojiAlreadyExistsException, EmojiNotFoundException
from .storage.model import Member, GuildMember, Guild, Role, MemberRole, Emoji
from .storage.uow import UnitOfWork
from ..security import Security
from ...log import Logger


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_discord_guild(self, guild_id: int) -> discord.Guild:
        discord_guild = self.uow.bot.get_guild(guild_id)

        if discord_guild is None:
            discord_guild = await self.uow.bot.fetch_guild(guild_id)

        if discord_guild is None:
            raise GuildNotFoundException(f"Could not find guild with id {guild_id}")

        return discord_guild

    async def get_discord_member(self, guild_id: int, member_id: int) -> discord.Member:
        discord_guild = await self.get_discord_guild(guild_id)
        discord_member = discord_guild.get_member(member_id)

        if discord_member is None:
            discord_member = await discord_guild.fetch_member(member_id)

        if discord_member is None:
            raise MemberNotFound(f"Could not find member with id {member_id} in guild {discord_guild.name}")

        return discord_member

    async def get_discord_role(self, guild_id: int, role_id: int) -> discord.Role:
        discord_guild = await self.get_discord_guild(guild_id)
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
        discord_guild = await self.get_discord_guild(guild_id)

        try:
            role = await discord_guild.create_role(name=name, colour=colour, hoist=hoist, reason=reason)
            return self.uow.role_repo.add(Role(role.id, discord_guild.id, role.name))
        except DiscordException as error:
            Logger.log(discord_guild.name, f"Failed to add role: {name}")
            raise error

    @Security.can_edit_roles()
    async def delete_role(self, guild_id: int, role_id: int, reason: str) -> None:
        try:
            discord_role = await self.get_discord_role(guild_id, role_id)
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
        discord_role = await self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.add_roles(discord_role, reason=reason)
            self.uow.member_role_repo.add(MemberRole(guild_id, member_id, role_id))
        except DiscordException as error:
            Logger.log(guild_id, f"Failed to add role {discord_role.name} ({discord_role.id}) to member {discord_member.name} ({discord_member.id})")
            raise error

    @Security.can_edit_roles()
    async def remove_role_from_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_member = await self.get_discord_member(guild_id, member_id)
        discord_role = await self.get_discord_role(guild_id, role_id)

        try:
            await discord_member.remove_roles(discord_role, reason=reason)

            role = self.uow.member_role_repo.get_by_guild_id_and_member_id_and_role_id(guild_id, member_id, role_id)

            if role is not None:
                self.uow.member_role_repo.remove(role)

        except DiscordException as error:
            Logger.log(guild_id, f"Failed to add role {discord_role.name} ({discord_role.id}) to member {discord_member.name} ({discord_member.id})")
            raise error

    async def enable_emoji(self, emoji_id: int, guild_id: int, emoji_name: str):
        if self.uow.emoji_repo.get_by_id(emoji_id) is not None:
            raise EmojiAlreadyExistsException("Emoji is already enabled!")
        self.uow.emoji_repo.add(Emoji(emoji_id, guild_id, emoji_name))

    async def disable_emoji(self, emoji_id: int):
        emoji = self.uow.emoji_repo.get_by_id(emoji_id)
        if emoji is None:
            raise EmojiNotFoundException("Emoji is already disabled!")
        self.uow.emoji_repo.remove(emoji)

    def get_emoji_by_id(self, emoji_id: int) -> Optional[Emoji]:
        emoji = self.uow.emoji_repo.get_by_id(emoji_id)

        if emoji is None:
            return None

        return self.uow.bot.get_emoji(emoji.id)

    def get_emoji_from_message(self, msg: str):
        emoji_text = re.search(r'^<\w*:\w*:(\d*)>$', msg)

        if emoji_text is None:
            return None

        return self.get_emoji_by_id(int(emoji_text.group(1)))

    async def get_random_enabled_emoji(self):
        emoji_list = self.uow.emoji_repo.get_all()
        emoji = None
        for i in range(10):
            test_emoji = emoji_list[random.randint(0, len(emoji_list) - 1)]
            emoji = self.uow.bot.get_emoji(test_emoji.id)
            if emoji is not None:
                break
        return emoji
