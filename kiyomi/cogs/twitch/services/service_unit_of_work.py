import twitchio
from twitchio.ext.eventsub import EventSubClient

from .message_service import MessageService
from .twitch_broadcaster_service import TwitchBroadcasterService
from .event_service import EventService
from ..storage import StorageUnitOfWork
from kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(
        self, bot: Kiyomi, storage_uow: StorageUnitOfWork, twitch_client: twitchio.Client, eventsub_client: EventSubClient
    ):
        super().__init__(storage_uow)

        self.events = EventService(bot, storage_uow, twitch_client, eventsub_client)
        self.messages = MessageService(bot, storage_uow)
        self.twitch_broadcasters = TwitchBroadcasterService(bot, storage_uow.twitch_broadcasters, storage_uow, twitch_client)
