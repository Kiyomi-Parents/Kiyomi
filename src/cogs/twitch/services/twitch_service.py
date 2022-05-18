import twitchio
from twitchio.ext.eventsub import EventSubClient

from ..storage.unit_of_work import UnitOfWork
from src.kiyomi import BaseService, Kiyomi


class TwitchService(BaseService[UnitOfWork]):
    twitch: twitchio.Client

    def __init__(self, bot: Kiyomi, uow: UnitOfWork, twitch_client: twitchio.Client, eventsub_client: EventSubClient):
        super().__init__(bot, uow)

        self.eventsub_client = eventsub_client
        self.twitch = twitch_client
