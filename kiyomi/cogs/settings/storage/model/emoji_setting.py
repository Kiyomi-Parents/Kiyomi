from typing import Optional, List

import discord
from discord import Permissions, Interaction
from discord.app_commands import Choice

from kiyomi import Kiyomi
from .abstract_bot_setting import AbstractBotSetting
from .enums.setting_type import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class EmojiSetting(AbstractBotSetting[discord.Emoji]):
    setting_type = SettingType.EMOJI

    @staticmethod
    def create(
        bot: Kiyomi,
        group: str,
        name_human: str,
        name: str,
        permissions: Optional[Permissions] = None,
        default_value: Optional[discord.Emoji] = None,
    ):
        if permissions is None:
            permissions = Permissions(manage_emojis=True)

        if default_value is not None:
            default_value = EmojiSetting.from_type(default_value)

        return EmojiSetting(
            bot,
            group,
            name_human,
            Setting(None, SettingType.EMOJI, name, default_value),
            permissions,
        )

    @property
    def value_human(self) -> str:
        return f":{self.value.name}:"

    @property
    def value(self) -> discord.Emoji:
        return self.to_type(self.bot, self.setting.value)

    @value.setter
    def value(self, value: Optional[str]):
        self.setting.value = self.from_type(value)

    @staticmethod
    def to_type(bot: Kiyomi, value: Optional[str]) -> Optional[discord.Emoji]:
        if value is None:
            return None

        return bot.get_emoji(int(value))

    @staticmethod
    def from_type(value: Optional[discord.Emoji]) -> Optional[str]:
        if value is None:
            return None

        return str(value.id)

    @staticmethod
    def get_from_setting(
        bot: Kiyomi,
        group: str,
        name_human: str,
        setting: Setting,
        permissions: Optional[Permissions] = None,
    ):
        if setting.setting_type is not SettingType.EMOJI:
            raise InvalidSettingType(setting.setting_type, SettingType.EMOJI)

        return EmojiSetting(bot, group, name_human, setting, permissions)

    @staticmethod
    async def is_valid(bot: Kiyomi, guild_id: int, value: str) -> bool:
        guild = bot.get_guild(guild_id)

        if guild is None:
            return False

        return value in [str(emoji.id) for emoji in await guild.fetch_emojis()]

    async def get_autocomplete(self, ctx: Interaction, current: str) -> List[Choice]:
        emojis = []

        if not self.has_permission(ctx.user):
            return emojis

        for emoji in await ctx.guild.fetch_emojis():
            if current.lower() not in emoji.name.lower():
                continue

            label = f"{emoji.name}"

            if self.value is not None and self.value.id == emoji.id:
                label += " [Current]"

            emojis.append(Choice(name=label, value=str(emoji.id)))

        return emojis
