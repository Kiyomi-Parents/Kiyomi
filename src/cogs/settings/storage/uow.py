from Kiyomi import Kiyomi
from .repository.settings_repository import SettingsRepository


class UnitOfWork:

    def __init__(self, bot: Kiyomi):
        self.settings_repo = SettingsRepository(bot.database)

        self.bot = bot
