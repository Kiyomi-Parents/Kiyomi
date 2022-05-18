from src.kiyomi import BaseCog, Kiyomi
from . import TwitchStreamerService, MessageService
from .services.event_service import TwitchEventService


class TwitchCog(BaseCog):
    def __init__(self, bot: Kiyomi, twitch_streamer_service: TwitchStreamerService, twitch_event_service: TwitchEventService, message_service: MessageService):
        super().__init__(bot)

        self.twitch_streamer_service = twitch_streamer_service
        self.twitch_event_service = twitch_event_service
        self.message_service = message_service
