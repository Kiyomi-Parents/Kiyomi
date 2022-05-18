from twitchio.ext.eventsub import StreamOnlineData


class TwitchStreamRepository:
    def __init__(self):
        self._live_streams = []

    def is_live(self, event: StreamOnlineData) -> bool:
        return event.broadcaster.id in [event.broadcaster.id for event in self._live_streams]

    def remove_by_broadcaster_id(self, broadcaster_id: int):
        broadcasters = list(filter(lambda event: event.broadcaster.id == broadcaster_id, self._live_streams))
        for broadcaster in broadcasters:
            self._live_streams.remove(broadcaster)

    def add(self, event: StreamOnlineData):
        if self.is_live(event):
            self.remove_by_broadcaster_id(event.broadcaster.id)
        self._live_streams.append(event)
