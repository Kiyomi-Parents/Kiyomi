from typing import Optional, List, Type

from sqlalchemy import select

from src.kiyomi.database import BaseRepository
from src.log import Logger
from ..model import Setting


class SettingsRepository(BaseRepository[Setting]):

    @property
    def _table(self) -> Type[Setting]:
        return Setting

    async def get_by_guild_id_and_name(self, guild_id: int, name: str) -> Optional[Setting]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.name == name)
        return await self._first(stmt)

    async def set(self, setting_id: int, value: str) -> Optional[Setting]:
        setting = await self.update(setting_id, {"value": value})

        Logger.log(setting, f"Set {setting.name} to {value}")
        return setting

    async def get_by_guild_id(self, guild_id: int) -> List[Setting]:
        stmt = select(self._table).where(self._table.guild_id == guild_id)
        return await self._all(stmt)
