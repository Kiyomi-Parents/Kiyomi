from sqlalchemy.ext.asyncio import AsyncSession

from kiyomi import BaseStorageUnitOfWork
from .repository.guild_twitch_broadcaster_repository import GuildTwitchBroadcasterRepository
from .repository.twitch_broadcast_repository import TwitchBroadcastRepository
from .repository.twitch_broadcaster_repository import TwitchBroadcasterRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.twitch_broadcasters = TwitchBroadcasterRepository(self._session)
        self.guild_twitch_broadcasters = GuildTwitchBroadcasterRepository(self._session)
        self.twitch_broadcasts = TwitchBroadcastRepository()
