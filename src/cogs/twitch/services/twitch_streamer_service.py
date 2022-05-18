from typing import List

from twitchio import User, ChannelInfo, Stream

from .twitch_service import TwitchService
from ..errors import TwitchStreamerNotFound, StreamNotFound
from ..storage.model.guild_twitch_streamer import GuildTwitchStreamer
from ..storage.model.twitch_streamer import TwitchStreamer


class TwitchStreamerService(TwitchService):

    async def get_user(self, login: str) -> User:
        users: List[User] = await self.twitch.fetch_users(names=[login])

        if len(users) == 0:
            raise TwitchStreamerNotFound(login)

        return users[0]

    async def register_twitch_streamer(self, guild_id: int, member_id: int, login: str) -> GuildTwitchStreamer:
        async with self.uow:
            twitch_streamer = await self.add_twitch_streamer(login)
            guild_twitch_streamer = await self.add_guild_twitch_streamer(guild_id, member_id, twitch_streamer.id)

        return guild_twitch_streamer

    async def add_twitch_streamer(self, login: str) -> TwitchStreamer:
        user = await self.get_user(login)

        async with self.uow:
            return await self.uow.twitch_streamers.upsert(TwitchStreamer(user))

    async def add_guild_twitch_streamer(self, guild_id: int, member_id: int, twitch_streamer_id: str) -> GuildTwitchStreamer:
        guild_twitch_streamers = await self.uow.guild_twitch_streamers.get_all_by_member_id(member_id)

        for guild_twitch_streamer in guild_twitch_streamers:
            if guild_twitch_streamer.guild_id == guild_id:
                streamer = await self.uow.guild_twitch_streamers.get_by_guild_id_and_member_id(guild_id, member_id)
                await self.uow.guild_twitch_streamers.remove_by_id(streamer.id)

        async with self.uow:
            return await self.uow.guild_twitch_streamers.add(GuildTwitchStreamer(guild_id, member_id, twitch_streamer_id))

    async def get_guild_twitch_streamers_by_twitch_streamer_id(self, twitch_streamer_id) -> List[GuildTwitchStreamer]:
        return await self.uow.guild_twitch_streamers.get_all_by_twitch_streamer_id(twitch_streamer_id)

    async def get_channel(self, channel_id_or_name: str) -> ChannelInfo:
        return await self.twitch.fetch_channel(channel_id_or_name)

    async def get_stream(self, user_id: int) -> Stream:
        streams = await self.twitch.fetch_streams(user_ids=[user_id])
        if len(streams) == 0:
            raise StreamNotFound(user_id)
        return streams[0]
