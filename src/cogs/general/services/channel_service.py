from typing import List, Union

from discord import Thread, NotFound
from discord.abc import GuildChannel, PrivateChannel

from .guild_service import GuildService
from ..errors import ChannelNotFoundException
from ..storage.model.channel import Channel
from ..storage.unit_of_work import UnitOfWork
from .general_service import GeneralService
from src.kiyomi import Kiyomi


class ChannelService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService):
        super().__init__(bot, uow)

        self.guild_service = guild_service

    async def get_discord_channel(self, channel_id: int) -> Union[GuildChannel, PrivateChannel, Thread]:
        discord_channel = self.bot.get_channel(channel_id)

        if discord_channel is None:
            try:
                discord_channel = await self.bot.fetch_channel(channel_id)
            except NotFound:
                raise ChannelNotFoundException(f"Could not find channel with id {channel_id}")

        if discord_channel is None:
            raise ChannelNotFoundException(f"Could not find channel with id {channel_id}")

        return discord_channel

    async def register_channel(self, guild_id: int, channel_id: int) -> Channel:
        async with self.uow:
            await self.guild_service.register_guild(guild_id)

            discord_channel = await self.get_discord_channel(channel_id)
            return await self.uow.channels.upsert(Channel(guild_id, channel_id, discord_channel.name))

    async def get_channels_in_guild(self, guild_id: int) -> List[Channel]:
        async with self.uow:
            guild = await self.uow.channels.get_all_by_guild_id(guild_id)

            return guild.channels
