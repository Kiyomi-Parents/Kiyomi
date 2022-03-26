from typing import Optional

import discord
from discord import OptionChoice

from .abstract_setting import AbstractSetting
from .enums import SettingType
from .setting import Setting
from ...errors import InvalidSettingTypeException


class EmojiSetting(AbstractSetting[discord.Emoji]):

    bot: discord.Bot

    def __init__(self, bot: discord.Bot, setting: Setting):
        self.bot = bot
        self.setting = setting

    @staticmethod
    def create(bot: discord.Bot, name: str, default_value: Optional[discord.Emoji]):
        if default_value is not None:
            default_value = EmojiSetting.from_type(default_value)

        return EmojiSetting(bot, Setting(None, SettingType.EMOJI, name, default_value))

    @property
    def value(self) -> discord.Emoji:
        return self.to_type(self.bot, self.setting.value)

    @value.setter
    def value(self, value: Optional[str]):
        self.setting.value = self.from_type(value)

    @staticmethod
    def to_type(bot: discord.Bot, value: Optional[str]) -> Optional[discord.Emoji]:
        if value is None:
            return None

        return bot.get_emoji(int(value))

    @staticmethod
    def from_type(value: Optional[discord.Emoji]) -> Optional[str]:
        if value is None:
            return None

        return str(value.id)

    @staticmethod
    def get_from_setting(bot: discord.Bot, setting: Setting):
        if setting.setting_type is not SettingType.EMOJI:
            raise InvalidSettingTypeException(f"Can't convert setting of type {setting.setting_type} to {SettingType.EMOJI}")

        return EmojiSetting(bot, setting)

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        emojis = []

        for emoji in await ctx.interaction.guild.fetch_emojis():
            label = f"{emoji.name}"

            if self.value is not None and self.value.id == emoji.id:
                label += ' (current)'

            emojis.append(OptionChoice(label, str(emoji.id)))

        return emojis