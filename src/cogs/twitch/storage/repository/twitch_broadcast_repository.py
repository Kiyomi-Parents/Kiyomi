from dataclasses import dataclass
from typing import List

from discord import Message
from twitchio import PartialUser
from twitchio.ext.eventsub import StreamOnlineData


@dataclass
class AnnouncedBroadcast:
    event: StreamOnlineData
    messages: List[Message]

    @property
    def broadcaster(self) -> PartialUser:
        return self.event.broadcaster


class TwitchBroadcastRepository:
    def __init__(self):
        self._broadcasts: List[AnnouncedBroadcast] = []

    def is_live(self, event: StreamOnlineData) -> bool:
        return event.broadcaster.id in [broadcast.broadcaster.id for broadcast in self._broadcasts]

    def remove_by_broadcaster_id(self, broadcaster_id: int) -> List[AnnouncedBroadcast]:
        broadcasts = [broadcast for broadcast in self._broadcasts if broadcaster_id == broadcast.broadcaster.id]
        for broadcast in broadcasts:
            self._broadcasts.remove(broadcast)

        return broadcasts

    def add(self, event: StreamOnlineData, messages: List[Message]):
        if self.is_live(event):
            self.remove_by_broadcaster_id(event.broadcaster.id)

        self._broadcasts.append(AnnouncedBroadcast(event, messages))
