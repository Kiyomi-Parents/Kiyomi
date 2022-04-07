from src.kiyomi import BaseCog, Kiyomi
from .services import SettingService, SettingAutocompleteService


class SettingsCog(BaseCog):
    def __init__(self, bot: Kiyomi, setting_service: SettingService, settings_autocomplete_service: SettingAutocompleteService):
        super().__init__(bot)

        self.setting_service = setting_service
        self.settings_autocomplete_service = settings_autocomplete_service
