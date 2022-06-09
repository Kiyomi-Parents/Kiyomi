from typing import List

import twitchio
from twitchio import User, ChannelInfo, Stream, HTTPException

from src.kiyomi import BaseService, Kiyomi
from ..errors import BroadcasterNotFound, BroadcastNotFound, GuildTwitchBroadcasterNotFound
from ..storage import StorageUnitOfWork
from ..storage.model.guild_twitch_broadcaster import GuildTwitchBroadcaster
from ..storage.model.twitch_broadcaster import TwitchBroadcaster
from ..storage.repository.twitch_broadcaster_repository import TwitchBroadcasterRepository


class TwitchBroadcasterService(BaseService[TwitchBroadcaster, TwitchBroadcasterRepository, StorageUnitOfWork]):
    def __init__(
        self,
        bot: Kiyomi,
        repository: TwitchBroadcasterRepository,
        storage_uow: StorageUnitOfWork,
        twitch_client: twitchio.Client,
    ):
        super().__init__(bot, repository, storage_uow)

        self.twitch_client = twitch_client

    async def fetch_user(self, login: str = None, user_id: int = None) -> User:
        fetch_kwargs = {}
        error_kwargs = {}
        if login is not None:
            fetch_kwargs["names"] = [login]
            error_kwargs["login"] = login
        elif user_id is not None:
            fetch_kwargs["ids"] = [user_id]
            error_kwargs["user_id"] = user_id
        else:
            raise BroadcasterNotFound()

        try:
            users: List[User] = await self.twitch_client.fetch_users(**fetch_kwargs)
        except HTTPException:
            users = []

        if len(users) == 0:
            raise BroadcasterNotFound(**error_kwargs)

        return users[0]

    async def register_twitch_broadcaster(self, guild_id: int, member_id: int, login: str) -> GuildTwitchBroadcaster:
        twitch_broadcaster = await self.add_twitch_broadcaster(login)
        guild_twitch_broadcaster = await self.add_guild_twitch_broadcaster(guild_id, member_id, twitch_broadcaster.id)

        return guild_twitch_broadcaster

    async def add_twitch_broadcaster(self, login: str) -> TwitchBroadcaster:
        user = await self.fetch_user(login=login)
        return await self.storage_uow.twitch_broadcasters.upsert(TwitchBroadcaster(user))

    async def add_guild_twitch_broadcaster(
        self, guild_id: int, member_id: int, broadcaster_id: str
    ) -> GuildTwitchBroadcaster:
        guild_twitch_broadcasters = await self.storage_uow.guild_twitch_broadcasters.get_all_by_member_id(member_id)

        for guild_twitch_broadcaster in guild_twitch_broadcasters:
            if guild_twitch_broadcaster.guild_id == guild_id:
                broadcaster = await self.storage_uow.guild_twitch_broadcasters.get_by_guild_id_and_member_id(
                    guild_id, member_id
                )
                await self.storage_uow.guild_twitch_broadcasters.remove_by_id(broadcaster.id)

        entity = await self.storage_uow.guild_twitch_broadcasters.add(
            GuildTwitchBroadcaster(guild_id, member_id, broadcaster_id)
        )

        return await self.storage_uow.refresh(entity)

    async def unregister_guild_twitch_broadcaster(self, guild_id: int, member_id: int) -> GuildTwitchBroadcaster:
        guild_twitch_broadcaster = await self.storage_uow.guild_twitch_broadcasters.delete_by_guild_id_and_member_id(
            guild_id, member_id
        )
        if guild_twitch_broadcaster is None:
            raise GuildTwitchBroadcasterNotFound(
                f"Couldn't find GuildTwitchBroadcaster with guild_id {guild_id}, member_id {member_id}"
            )
        twitch_broadcaster = guild_twitch_broadcaster.twitch_broadcaster

        await self.storage_uow.refresh(twitch_broadcaster)

        if len(twitch_broadcaster.guilds) == 0:
            await self.storage_uow.twitch_broadcasters.remove(twitch_broadcaster)

        return guild_twitch_broadcaster

    async def get_all_by_broadcaster_id(self, broadcaster_id) -> List[GuildTwitchBroadcaster]:
        return await self.storage_uow.guild_twitch_broadcasters.get_all_by_broadcaster_id(broadcaster_id)

    async def fetch_channel(self, channel_id_or_name: str) -> ChannelInfo:
        return await self.twitch_client.fetch_channel(channel_id_or_name)

    async def fetch_stream(self, broadcaster_id: int) -> Stream:
        streams = await self.twitch_client.fetch_streams(user_ids=[broadcaster_id])
        if len(streams) == 0:
            raise BroadcastNotFound(broadcaster_id)
        return streams[0]
