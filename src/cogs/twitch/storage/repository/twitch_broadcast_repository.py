from typing import List

from twitchio.ext.eventsub import StreamOnlineData


class TwitchBroadcastRepository:
    def __init__(self):
        self._broadcasts: List[StreamOnlineData] = []

    def is_live(self, event: StreamOnlineData) -> bool:
        return event.broadcaster.id in [event.broadcaster.id for event in self._broadcasts]

    def remove_by_broadcaster_id(self, broadcaster_id: int):
        broadcasters = list(filter(lambda event: event.broadcaster.id == broadcaster_id, self._broadcasts))
        for broadcaster in broadcasters:
            self._broadcasts.remove(broadcaster)

    def add(self, event: StreamOnlineData):
        if self.is_live(event):
            self.remove_by_broadcaster_id(event.broadcaster.id)
        self._broadcasts.append(event)
