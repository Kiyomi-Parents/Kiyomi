from src.kiyomi import Kiyomi
from .services import SettingService, SettingAutocompleteService
from .settings import Settings
from .settings_api import SettingsAPI
from .storage import UnitOfWork


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    setting_service = SettingService(bot, uow)
    settings_autocomplete_service = SettingAutocompleteService(bot, uow, setting_service)

    bot.add_cog(Settings(bot, setting_service, settings_autocomplete_service))
    bot.add_cog(SettingsAPI(bot, setting_service, settings_autocomplete_service, uow))
