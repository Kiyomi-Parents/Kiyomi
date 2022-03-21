from typing import Optional

from src.kiyomi import Kiyomi
from .services import SettingService
from .settings_cog import SettingsCog
from .storage.uow import UnitOfWork


class SettingsAPI(SettingsCog):

    def __init__(self, bot: Kiyomi, setting_service: SettingService, uow: UnitOfWork):
        super().__init__(bot, setting_service)

        self.uow = uow

    def set(self, guild_id: int, name: str, value: any) -> None:
        self.setting_service.set(guild_id, name, value)

    def get(self, guild_id: int, name: str) -> Optional[any]:
        return self.setting_service.get_value(guild_id, name)

    def delete(self, guild_id: int, name: str) -> None:
        self.setting_service.delete(guild_id, name)
