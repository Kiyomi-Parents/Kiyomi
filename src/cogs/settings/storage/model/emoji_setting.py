from typing import Optional

import discord
from discord import OptionChoice, Permissions

from src.kiyomi import Kiyomi
from .abstract_bot_setting import AbstractBotSetting
from .enums import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class EmojiSetting(AbstractBotSetting[discord.Emoji]):
    setting_type = SettingType.EMOJI

    @staticmethod
    def create(
        bot: Kiyomi,
        name_human: str,
        name: str,
        permissions: Optional[Permissions] = None,
        default_value: Optional[discord.Emoji] = None
    ):
        if permissions is None:
            permissions = Permissions(manage_emojis=True)

        if default_value is not None:
            default_value = EmojiSetting.from_type(default_value)

        return EmojiSetting(
                bot,
                name_human,
                Setting(None, SettingType.EMOJI, name, default_value),
                permissions
        )

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
        name_human: str,
        setting: Setting,
        permissions: Optional[Permissions] = None
    ):
        if setting.setting_type is not SettingType.EMOJI:
            raise InvalidSettingType(setting.setting_type, SettingType.EMOJI)

        return EmojiSetting(bot, name_human, setting, permissions)

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        emojis = []

        if not self.has_permission(ctx.interaction.user):
            return emojis

        for emoji in await ctx.interaction.guild.fetch_emojis():
            if ctx.value.lower() not in emoji.name.lower():
                continue

            label = f"{emoji.name}"

            if self.value is not None and self.value.id == emoji.id:
                label += ' (current)'

            emojis.append(OptionChoice(label, str(emoji.id)))

        return emojis