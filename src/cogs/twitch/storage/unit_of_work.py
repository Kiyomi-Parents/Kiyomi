from sqlalchemy.ext.asyncio import AsyncSession

from .repository.guild_twitch_broadcaster_repository import GuildTwitchBroadcasterRepository
from .repository.twitch_broadcast_repository import TwitchBroadcastRepository
from .repository.twitch_broadcaster_repository import TwitchBroadcasterRepository
from src.kiyomi import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.twitch_broadcasters = TwitchBroadcasterRepository(session)
        self.guild_twitch_broadcasters = GuildTwitchBroadcasterRepository(session)
        self.twitch_broadcasts = TwitchBroadcastRepository()
