from sqlalchemy.ext.asyncio import AsyncSession

from .repository.guild_twitch_streamer_repository import GuildTwitchStreamerRepository
from .repository.twitch_stream_repository import TwitchStreamRepository
from .repository.twitch_streamer_repository import TwitchStreamerRepository
from src.kiyomi import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.twitch_streamers = TwitchStreamerRepository(session)
        self.guild_twitch_streamers = GuildTwitchStreamerRepository(session)
        self.twitch_streams = TwitchStreamRepository()
