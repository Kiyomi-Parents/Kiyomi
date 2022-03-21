from .services import SettingService
from src.kiyomi import BaseCog, Kiyomi


class SettingsCog(BaseCog):
    def __init__(self, bot: Kiyomi, setting_service: SettingService):
        super().__init__(bot)

        self.setting_service = setting_service
