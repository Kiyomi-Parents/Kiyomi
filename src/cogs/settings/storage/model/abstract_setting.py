from abc import ABC
from typing import TypeVar, Generic, Optional, List

from discord import Permissions, Member, Interaction
from discord.app_commands import Choice

from .enums.setting_type import SettingType
from .setting import Setting

T = TypeVar("T")


class AbstractSetting(ABC, Generic[T]):
    setting_type: SettingType
    setting: Setting
    permissions: Optional[Permissions] = None

    def __init__(
        self,
        name_human: str,
        setting: Setting,
        permissions: Optional[Permissions] = None,
    ):
        self.setting = setting
        self.name_human = name_human
        self.permissions = permissions

    def set(self, value: str) -> None:
        self.setting.value = value

    @property
    def value(self) -> T:
        return self.setting.value

    @value.setter
    def value(self, value: T) -> None:
        self.setting.value = value

    @property
    def name(self) -> str:
        return self.setting.name

    @property
    def type(self) -> SettingType:
        return self.setting.setting_type

    @property
    def guild_id(self) -> int:
        return self.setting.guild_id

    def has_permission(self, member: Member) -> bool:
        if self.permissions is not None:
            return member.guild_permissions.is_superset(self.permissions)

        return True

    async def get_autocomplete(self, ctx: Interaction, current: str) -> List[Choice]:
        if not self.has_permission(ctx.user):
            return []

        if self.setting.value is None:
            return []

        return [Choice(name=f"{self.setting.value} (current)", value=self.setting.value)]
