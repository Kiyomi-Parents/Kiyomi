from typing import List

from twitchio import User, ChannelInfo, Stream, HTTPException

from .twitch_service import TwitchService
from ..errors import BroadcasterNotFound, BroadcastNotFound, GuildTwitchBroadcasterNotFound
from ..storage.model.guild_twitch_broadcaster import GuildTwitchBroadcaster
from ..storage.model.twitch_broadcaster import TwitchBroadcaster


class BroadcasterService(TwitchService):

    async def fetch_user(self, login: str) -> User:
        try:
            users: List[User] = await self.twitch_client.fetch_users(names=[login])
        except HTTPException:
            raise BroadcasterNotFound(login)

        if len(users) == 0:
            raise BroadcasterNotFound(login)

        return users[0]

    async def register_twitch_broadcaster(self, guild_id: int, member_id: int, login: str) -> GuildTwitchBroadcaster:
        async with self.uow:
            twitch_broadcaster = await self.add_twitch_broadcaster(login)
            guild_twitch_broadcaster = await self.add_guild_twitch_broadcaster(guild_id, member_id, twitch_broadcaster.id)

        return guild_twitch_broadcaster

    async def add_twitch_broadcaster(self, login: str) -> TwitchBroadcaster:
        user = await self.fetch_user(login)

        async with self.uow:
            return await self.uow.twitch_broadcasters.upsert(TwitchBroadcaster(user))

    async def add_guild_twitch_broadcaster(self, guild_id: int, member_id: int, broadcaster_id: str) -> GuildTwitchBroadcaster:
        guild_twitch_broadcasters = await self.uow.guild_twitch_broadcasters.get_all_by_member_id(member_id)

        for guild_twitch_broadcaster in guild_twitch_broadcasters:
            if guild_twitch_broadcaster.guild_id == guild_id:
                broadcaster = await self.uow.guild_twitch_broadcasters.get_by_guild_id_and_member_id(guild_id, member_id)
                await self.uow.guild_twitch_broadcasters.remove_by_id(broadcaster.id)

        async with self.uow:
            entity = await self.uow.guild_twitch_broadcasters.add(GuildTwitchBroadcaster(guild_id, member_id, broadcaster_id))
        return await self.uow.refresh(entity)

    async def unregister_guild_twitch_broadcaster(self, guild_id: int, member_id: int) -> GuildTwitchBroadcaster:
        async with self.uow:
            guild_twitch_broadcaster = await self.uow.guild_twitch_broadcasters.remove_by_guild_id_and_member_id(guild_id, member_id)
            if guild_twitch_broadcaster is None:
                raise GuildTwitchBroadcasterNotFound(f"Couldn't find GuildTwitchBroadcaster with guild_id {guild_id}, member_id {member_id}")
            return guild_twitch_broadcaster

    async def get_guild_twitch_broadcasters_by_broadcaster_id(self, broadcaster_id) -> List[GuildTwitchBroadcaster]:
        return await self.uow.guild_twitch_broadcasters.get_all_by_broadcaster_id(broadcaster_id)

    async def fetch_channel(self, channel_id_or_name: str) -> ChannelInfo:
        return await self.twitch_client.fetch_channel(channel_id_or_name)

    async def fetch_stream(self, broadcaster_id: int) -> Stream:
        streams = await self.twitch_client.fetch_streams(user_ids=[broadcaster_id])
        if len(streams) == 0:
            raise BroadcastNotFound(broadcaster_id)
        return streams[0]
