from typing import Optional, List

import discord

from src.kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .storage.model.abstract_setting import AbstractSetting


class SettingsAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def set(self, guild_id: int, name: str, value: any) -> AbstractSetting:
        setting = await self.service_uow.settings.set(guild_id, name, value)
        await self.service_uow.save_changes()

        return setting

    async def get(self, guild_id: int, name: str) -> Optional[any]:
        return await self.service_uow.settings.get_value(guild_id, name)

    async def get_setting(self, guild_id: int, name: str) -> AbstractSetting:
        return await self.service_uow.settings.get(guild_id, name)

    def get_registered(self) -> List[AbstractSetting]:
        return self.service_uow.settings.registered_settings

    def has_permission(self, name: str, discord_member: discord.Member) -> bool:
        return self.service_uow.settings.has_permission(name, discord_member)

    async def validate_setting_value(self, guild_id: int, name: str, value: Optional[str]):
        return await self.service_uow.settings.validate_setting_value(guild_id, name, value)

    async def delete(self, guild_id: int, name: str) -> AbstractSetting:
        setting = await self.service_uow.settings.delete(guild_id, name)
        await self.service_uow.save_changes()

        return setting

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
