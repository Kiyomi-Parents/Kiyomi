from typing import Optional

from src.kiyomi import Kiyomi
from .services import SettingService, SettingAutocompleteService
from .settings_cog import SettingsCog
from .storage import AbstractSetting
from .storage.uow import UnitOfWork


class SettingsAPI(SettingsCog):

    def __init__(
            self,
            bot: Kiyomi,
            setting_service: SettingService,
            settings_autocomplete_service: SettingAutocompleteService,
            uow: UnitOfWork
    ):
        super().__init__(bot, setting_service, settings_autocomplete_service)

        self.uow = uow

    def set(self, guild_id: int, name: str, value: any) -> None:
        self.setting_service.set(guild_id, name, value)

    def get(self, guild_id: int, name: str) -> Optional[any]:
        return self.setting_service.get_value(guild_id, name)

    def delete(self, guild_id: int, name: str) -> None:
        self.setting_service.delete(guild_id, name)

    async def get_override_or_default(
            self,
            guild_id: Optional[int],
            name: Optional[str]
    ) -> Optional[AbstractSetting]:
        if name is None:
            return None

        if guild_id is None:
            guild_id = self.bot.default_guild.id

        if guild_id is None:
            return None

        setting = self.get(guild_id, name)

        if setting is None and guild_id is not self.bot.default_guild.id:
            setting = self.get(self.bot.default_guild.id, name)

        return setting
