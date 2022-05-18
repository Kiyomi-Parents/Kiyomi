from typing import Type

from src.kiyomi.database import BaseRepository
from ..model.twitch_streamer import TwitchStreamer


class TwitchStreamerRepository(BaseRepository[TwitchStreamer]):

    @property
    def _table(self) -> Type[TwitchStreamer]:
        return TwitchStreamer
