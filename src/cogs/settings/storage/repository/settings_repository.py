from typing import Optional, List

from src.database import Repository
from src.log import Logger
from ..model import Setting


class SettingsRepository(Repository):

    def get_all(self) -> Optional[List[Setting]]:
        return self._db.session.query(Setting) \
            .all()

    def get_by_id(self, setting_id: int) -> Optional[Setting]:
        return self._db.session.query(Setting) \
            .filter(Setting.id == setting_id) \
            .first()

    def find(self, guild_id: int, name: str) -> Optional[Setting]:
        return self._db.session.query(Setting) \
            .filter(Setting.guild_id == guild_id) \
            .filter(Setting.name == name) \
            .first()

    def set(self, setting: Setting, value: str):
        setting.value = value

        self._db.commit_changes()
        Logger.log(setting, f"Set {setting.name} to {value}")
