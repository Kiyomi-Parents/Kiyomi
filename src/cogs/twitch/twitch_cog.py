from src.kiyomi import BaseCog, Kiyomi
from . import BroadcasterService, MessageService
from .services.event_service import EventService


class TwitchCog(BaseCog):
    def __init__(self, bot: Kiyomi, twitch_broadcaster_service: BroadcasterService, twitch_event_service: EventService, message_service: MessageService):
        super().__init__(bot)

        self.twitch_broadcaster_service = twitch_broadcaster_service
        self.twitch_event_service = twitch_event_service
        self.message_service = message_service
