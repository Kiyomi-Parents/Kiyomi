from src.kiyomi import BaseCog, Kiyomi
from . import BroadcasterService, MessageService
from .services.event_service import EventService


class TwitchCog(BaseCog):
    def __init__(self, bot: Kiyomi, broadcaster_service: BroadcasterService, event_service: EventService, message_service: MessageService):
        super().__init__(bot)

        self.broadcaster_service = broadcaster_service
        self.event_service = event_service
        self.message_service = message_service
