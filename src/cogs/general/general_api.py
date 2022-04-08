from typing import Optional, List

import discord
from discord import Colour, Emoji

from src.kiyomi import Kiyomi
from .errors import RoleNotFoundException
from .general_cog import GeneralCog
from .services import EmojiService, GuildService, MemberService, RoleService, ChannelService, MessageService
from .storage import UnitOfWork
from .storage.model.channel import Channel
from .storage.model.guild import Guild
from .storage.model.member import Member
from .storage.model.message import Message
from .storage.model.role import Role


class GeneralAPI(GeneralCog):
    def __init__(
            self,
            bot: Kiyomi,
            emoji_service: EmojiService,
            guild_service: GuildService,
            member_service: MemberService,
            channel_service: ChannelService,
            message_service: MessageService,
            role_service: RoleService,
            uow: UnitOfWork
    ):
        super().__init__(
                bot,
                emoji_service,
                guild_service,
                member_service,
                channel_service,
                message_service,
                role_service
        )

        self.uow = uow

    def get_guild(self, guild_id: int) -> Optional[Guild]:
        return self.uow.guilds.get_by_id(guild_id)

    def get_guilds(self) -> Optional[List[Guild]]:
        return self.uow.guilds.get_all()

    def get_member(self, member_id: int) -> Optional[Member]:
        return self.uow.members.get_by_id(member_id)

    async def get_discord_member(self, guild_id: int, member_id: int) -> Optional[discord.Member]:
        return await self.member_service.get_discord_member(guild_id, member_id)

    def get_all_guild_members(self) -> Optional[List[Member]]:
        return self.uow.guild_members.get_all()

    def get_members_in_guild(self, guild_id: int) -> Optional[List[Member]]:
        return self.uow.guild_members.get_all_by_guild_id(guild_id)

    async def create_role(self, guild_id: int, name: str, colour: Colour, hoist: bool, reason: str) -> Role:
        return await self.role_service.create_role(guild_id, name, colour, hoist, reason)

    async def delete_role(self, guild_id: int, role_id: int, reason: str) -> None:
        await self.role_service.delete_role(guild_id, role_id, reason)

    async def add_role_to_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        await self.role_service.add_role_to_member(guild_id, member_id, role_id, reason)

    async def remove_role_from_member(self, guild_id: int, member_id: int, role_id: int, reason: str) -> None:
        await self.role_service.remove_role_from_member(guild_id, member_id, role_id, reason)

    async def get_role(self, guild_id: int, role_id: int) -> Optional[Role]:
        try:
            return await self.role_service.get_discord_role(guild_id, role_id)
        except RoleNotFoundException:
            return None

    async def register_message(self, guild_id: int, channel_id: int, message_id: int) -> Message:
        return await self.message_service.register_message(guild_id, channel_id, message_id)

    async def get_guild_channels(self, guild_id: int) -> List[Channel]:
        return await self.channel_service.get_channels_in_guild(guild_id)

    async def get_channel_messages(self, channel_id: int) -> List[Message]:
        return await self.message_service.get_messages_in_channel(channel_id)

    async def register_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> Emoji:
        return await self.emoji_service.register_emoji(guild_id, emoji_id, emoji_name)

    async def unregister_emoji(self, guild_id: int, emoji_id: int) -> Emoji:
        return await self.emoji_service.unregister_emoji(guild_id, emoji_id)

    def get_emoji(self, emoji_name: str) -> Optional[Emoji]:
        emoji_name = emoji_name.replace(":", "")
        emoji = self.bot.get_emoji(self.uow.emojis.get_by_name(emoji_name).id)
        return emoji
