from .services import SettingService
from .settings import Settings
from .settings_api import SettingsAPI
from .storage import UnitOfWork
from src.kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    setting_service = SettingService(bot, uow)

    bot.add_cog(Settings(bot, setting_service))
    bot.add_cog(SettingsAPI(bot, setting_service, uow))
