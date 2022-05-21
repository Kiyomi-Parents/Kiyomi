from typing import Type

from src.kiyomi.database import BaseRepository
from ..model.twitch_broadcaster import TwitchBroadcaster


class TwitchBroadcasterRepository(BaseRepository[TwitchBroadcaster]):

    @property
    def _table(self) -> Type[TwitchBroadcaster]:
        return TwitchBroadcaster
