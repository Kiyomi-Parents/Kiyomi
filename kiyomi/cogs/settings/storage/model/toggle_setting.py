import distutils.util
from typing import Optional, List

from discord import Permissions, Interaction
from discord.app_commands import Choice

from .abstract_regular_setting import AbstractRegularSetting
from .enums.setting_type import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class ToggleSetting(AbstractRegularSetting[bool]):
    setting_type = SettingType.BOOLEAN

    @staticmethod
    def create(
        group: str,
        name_human: str,
        name: str,
        permissions: Optional[Permissions] = None,
        default_value: Optional[bool] = None,
    ):
        if default_value is not None:
            default_value = ToggleSetting.from_type(default_value)

        return ToggleSetting(
            group,
            name_human,
            Setting(None, SettingType.BOOLEAN, name, default_value),
            permissions,
        )

    @property
    def value(self) -> bool:
        return self.to_type(self.setting.value)

    @value.setter
    def value(self, value: bool):
        self.setting._value = self.from_type(value)

    @staticmethod
    def to_type(value: Optional[str]) -> Optional[bool]:
        if value is None:
            return None

        return bool(distutils.util.strtobool(value))

    @staticmethod
    def from_type(value: Optional[bool]) -> Optional[str]:
        if value is None:
            return None

        return str(value)

    @staticmethod
    def get_from_setting(group: str, name_human: str, setting: Setting, permissions: Optional[Permissions] = None):
        if setting.setting_type is not SettingType.BOOLEAN:
            raise InvalidSettingType(setting.setting_type, SettingType.BOOLEAN)

        return ToggleSetting(group, name_human, setting, permissions)

    @staticmethod
    async def is_valid(value: str) -> bool:
        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return True

        return False

    async def get_autocomplete(self, ctx: Interaction, current: str) -> List[Choice]:
        if not self.has_permission(ctx.user):
            return []

        return [
            Choice(name=f"Enabled{' [Current]' if self.value else ''}", value="True"),
            Choice(name=f"Disabled{' [Current]' if not self.value else ''}", value="False"),
        ]
