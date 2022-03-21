from typing import Optional

import discord.abc
from discord import OptionChoice

from ...errors import InvalidSettingTypeException
from .setting import Setting
from .abstract_setting import AbstractSetting
from .enums.setting_type import SettingType


class ChannelSetting(AbstractSetting[discord.abc.GuildChannel]):

    bot: discord.Bot

    def __init__(self, bot: discord.Bot, setting: Setting):
        self.bot = bot
        self.setting = setting

    @staticmethod
    def create(bot: discord.Bot, name: str, default_value: Optional[discord.abc.GuildChannel]):
        if default_value is not None:
            default_value = ChannelSetting.from_type(default_value)

        return ChannelSetting(bot, Setting(None, SettingType.CHANNEL, name, default_value))

    @property
    def value(self) -> discord.abc.GuildChannel:
        return self.to_type(self.bot, self.setting.value)

    @value.setter
    def value(self, value: Optional[str]):
        self.setting.value = self.from_type(value)

    @staticmethod
    def to_type(bot: discord.Bot, value: Optional[str]) -> Optional[discord.abc.GuildChannel]:
        if value is None:
            return None

        return bot.get_channel(int(value))

    @staticmethod
    def from_type(value: Optional[discord.abc.GuildChannel]) -> Optional[str]:
        if value is None:
            return None

        return str(value.id)

    @staticmethod
    def get_from_setting(bot: discord.Bot, setting: Setting):
        if setting.setting_type is not SettingType.CHANNEL:
            raise InvalidSettingTypeException(f"Can't convert setting of type {setting.setting_type} to {SettingType.CHANNEL}")

        return ChannelSetting(bot, setting)

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        text_channels = []

        for channel in await ctx.interaction.guild.fetch_channels():
            if isinstance(channel, discord.TextChannel):
                label = f"#{channel.name}"

                if self.value is not None and self.value.id == channel.id:
                    label += ' (current)'

                text_channels.append(OptionChoice(label, str(channel.id)))

        return text_channels
