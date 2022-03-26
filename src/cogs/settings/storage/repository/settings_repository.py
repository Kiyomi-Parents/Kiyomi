from typing import Optional, List

from sqlalchemy.orm import Query

from src.kiyomi.database import BaseRepository
from src.log import Logger
from ..model import Setting


class SettingsRepository(BaseRepository[Setting]):

    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Setting) \
            .filter(Setting.id == entry_id)

    def get_all(self) -> Optional[List[Setting]]:
        return self.session.query(Setting) \
            .all()

    def get_by_guild_id_and_name(self, guild_id: int, name: str) -> Optional[Setting]:
        return self.session.query(Setting) \
            .filter(Setting.guild_id == guild_id) \
            .filter(Setting.name == name) \
            .first()

    def set(self, setting: Setting, value: str):
        setting.value = value

        self.commit_changes()
        Logger.log(setting, f"Set {setting.name} to {value}")

    def get_by_guild_id(self, guild_id: int) -> Optional[List[Setting]]:
        return self.session.query(Setting) \
            .filter(Setting.guild_id == guild_id) \
            .all()
