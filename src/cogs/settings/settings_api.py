from typing import Optional

from src.kiyomi import Kiyomi
from .services import SettingService
from .settings_cog import SettingsCog
from .storage import AbstractSetting
from .storage.unit_of_work import UnitOfWork


class SettingsAPI(SettingsCog):
    def __init__(self, bot: Kiyomi, setting_service: SettingService, uow: UnitOfWork):
        super().__init__(bot, setting_service)

        self.uow = uow

    async def set(self, guild_id: int, name: str, value: any) -> AbstractSetting:
        return await self.setting_service.set(guild_id, name, value)

    async def get(self, guild_id: int, name: str) -> Optional[any]:
        return await self.setting_service.get_value(guild_id, name)

    async def delete(self, guild_id: int, name: str) -> AbstractSetting:
        return await self.setting_service.delete(guild_id, name)

    async def get_override_or_default(self, guild_id: Optional[int], name: Optional[str]) -> Optional[AbstractSetting]:
        if name is None:
            return None

        if guild_id is None:
            guild_id = self.bot.default_guild.id

        if guild_id is None:
            return None

        setting = await self.get(guild_id, name)

        if setting is None and guild_id is not self.bot.default_guild.id:
            setting = await self.get(self.bot.default_guild.id, name)

        return setting
