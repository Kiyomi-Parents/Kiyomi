from twitchAPI import Twitch

from src.cogs.twitch.storage.unit_of_work import UnitOfWork
from src.kiyomi import BaseService, Kiyomi


class TwitchService(BaseService[UnitOfWork]):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)

        self.twitch = Twitch('my_app_key', 'my_app_secret')
