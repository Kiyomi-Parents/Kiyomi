from src.kiyomi import Kiyomi
from .services import SettingService
from .settings import Settings
from .settings_api import SettingsAPI
from .storage import UnitOfWork


async def setup(bot: Kiyomi):
    uow = UnitOfWork(await bot.database.get_session())

    setting_service = SettingService(bot, uow)

    await bot.add_cog(Settings(bot, setting_service))
    await bot.add_cog(SettingsAPI(bot, setting_service, uow))
