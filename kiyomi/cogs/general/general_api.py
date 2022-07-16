from typing import Optional, List

import discord
from discord import Colour, Emoji

from kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .storage.model.channel import Channel
from .storage.model.guild import Guild
from .storage.model.guild_member import GuildMember
from .storage.model.member import Member
from .storage.model.member_role import MemberRole
from .storage.model.message import Message
from .storage.model.role import Role


class GeneralAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def get_guild(self, guild_id: int) -> Optional[Guild]:
        guild = await self.service_uow.guilds.get_by_id(guild_id)
        await self.service_uow.save_changes()

        return guild

    async def get_guilds(self) -> List[Guild]:
        guilds = await self.service_uow.guilds.get_all()
        await self.service_uow.save_changes()

        return guilds

    async def get_member(self, member_id: int) -> Optional[Member]:
        member = await self.service_uow.members.get_by_id(member_id)
        await self.service_uow.save_changes()

        return member

    async def register_member(self, guild_id: int, member_id: int):
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        await self.service_uow.members.upsert_member(discord_guild, member_id)
        await self.service_uow.members.register_guild_member(guild_id, member_id)
        await self.service_uow.save_changes()

    async def get_discord_member(self, guild_id: int, member_id: int) -> Optional[discord.Member]:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        discord_member = await self.service_uow.members.get_discord_member(discord_guild, member_id)
        await self.service_uow.save_changes()

        return discord_member

    async def get_all_guild_members(self) -> List[GuildMember]:
        guild_members = await self.service_uow.guild_members.get_all()
        await self.service_uow.save_changes()

        return guild_members

    async def get_members_in_guild(self, guild_id: int) -> List[GuildMember]:
        guild_members = await self.service_uow.guild_members.get_all_by_guild_id(guild_id)
        await self.service_uow.save_changes()

        return guild_members

    async def create_role(self, guild_id: int, name: str, colour: Colour, hoist: bool, reason: str) -> Role:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        role = await self.service_uow.roles.create_role(discord_guild, name, colour, hoist, reason)
        await self.service_uow.save_changes()

        return role

    async def delete_role(self, guild_id: int, role_id: int, reason: str) -> None:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        await self.service_uow.roles.delete_role(discord_guild, role_id, reason)
        await self.service_uow.save_changes()

    async def add_role_to_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> MemberRole:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        discord_member = await self.service_uow.members.upsert_member(discord_guild, member_id)
        discord_role = await self.service_uow.roles.get_discord_role(discord_guild, role_id)
        member_role = await self.service_uow.roles.add_role_to_member(discord_member, discord_role, reason)
        await self.service_uow.save_changes()

        return member_role

    async def remove_role_from_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        discord_member = await self.service_uow.members.upsert_member(discord_guild, member_id)
        discord_role = await self.service_uow.roles.get_discord_role(discord_guild, role_id)
        await self.service_uow.roles.remove_role_from_member(discord_member, discord_role, reason)
        await self.service_uow.save_changes()

    async def get_role(self, guild_id: int, role_id: int) -> Optional[Role]:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        role = await self.service_uow.roles.get_discord_role(discord_guild, role_id)
        await self.service_uow.save_changes()

        return role

    async def member_has_role(self, guild_id, member_id: int, role_id: int) -> bool:
        discord_guild = await self.service_uow.guilds.upsert_guild(guild_id)
        discord_member = await self.service_uow.members.get_discord_member(discord_guild, member_id)
        status = await self.service_uow.roles.member_has_role(discord_member, role_id)
        await self.service_uow.save_changes()

        return status

    async def register_message(self, guild_id: int, channel_id: int, message_id: int) -> Message:
        await self.service_uow.guilds.upsert_guild(guild_id)
        await self.service_uow.channels.upsert_channel(guild_id, channel_id)
        message = await self.service_uow.messages.register_message(guild_id, channel_id, message_id)
        await self.service_uow.save_changes()

        return message

    async def get_guild_channels(self, guild_id: int) -> List[Channel]:
        channels = await self.service_uow.channels.get_channels_in_guild(guild_id)
        await self.service_uow.save_changes()

        return channels

    async def get_channel_messages(self, channel_id: int) -> List[Message]:
        messages = await self.service_uow.messages.get_messages_in_channel(channel_id)
        await self.service_uow.save_changes()

        return messages

    async def register_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> Emoji:
        await self.service_uow.guilds.upsert_guild(guild_id)
        emoji = await self.service_uow.emojis.register_emoji(guild_id, emoji_id, emoji_name)
        await self.service_uow.save_changes()

        return emoji

    async def unregister_emoji(self, guild_id: int, emoji_id: int):
        await self.service_uow.emojis.unregister_emoji(guild_id, emoji_id)
        await self.service_uow.save_changes()

    async def get_emoji(self, emoji_name: str) -> Optional[Emoji]:
        emoji_name = emoji_name.replace(":", "")
        emoji = await self.service_uow.emojis.get_by_name(emoji_name)

        return self.bot.get_emoji(emoji.id)
