from typing import List, Union

from discord import Thread, NotFound
from discord.abc import GuildChannel, PrivateChannel

from ..errors import ChannelNotFoundException
from ..storage.model.channel import Channel
from ..storage.repository.channel_repository import ChannelRepository
from ..storage.storage_unit_of_work import StorageUnitOfWork
from kiyomi import BaseService


class ChannelService(BaseService[Channel, ChannelRepository, StorageUnitOfWork]):
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
        discord_channel = await self.get_discord_channel(channel_id)
        return await self.repository.upsert(Channel(guild_id, channel_id, discord_channel.name))

    async def upsert_channel(self, guild_id: int, channel_id: int) -> Union[GuildChannel, PrivateChannel, Thread]:
        discord_channel = await self.get_discord_channel(channel_id)
        await self.repository.upsert(Channel(guild_id, channel_id, discord_channel.name))

        return discord_channel

    async def get_channels_in_guild(self, guild_id: int) -> List[Channel]:
        return await self.repository.get_all_by_guild_id(guild_id)
