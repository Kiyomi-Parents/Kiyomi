from typing import Optional

import discord.abc
from discord import OptionChoice, Permissions

from src.kiyomi import Kiyomi
from .abstract_bot_setting import AbstractBotSetting
from .enums.setting_type import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class ChannelSetting(AbstractBotSetting[discord.abc.GuildChannel]):
    setting_type = SettingType.CHANNEL

    @staticmethod
    def create(
        bot: Kiyomi,
        name_human: str,
        name: str,
        permissions: Optional[Permissions] = None,
        default_value: Optional[discord.abc.GuildChannel] = None
    ):
        if permissions is None:
            permissions = Permissions(manage_channels=True)

        if default_value is not None:
            default_value = ChannelSetting.from_type(default_value)

        return ChannelSetting(
                bot,
                name_human,
                Setting(None, SettingType.CHANNEL, name, default_value),
                permissions
        )

    @property
    def value(self) -> discord.abc.GuildChannel:
        return self.to_type(self.bot, self.setting.value)

    @value.setter
    def value(self, value: Optional[str]):
        self.setting.value = self.from_type(value)

    @staticmethod
    def to_type(bot: Kiyomi, value: Optional[str]) -> Optional[discord.abc.GuildChannel]:
        if value is None:
            return None

        return bot.get_channel(int(value))

    @staticmethod
    def from_type(value: Optional[discord.abc.GuildChannel]) -> Optional[str]:
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
        if setting.setting_type is not SettingType.CHANNEL:
            raise InvalidSettingType(setting.setting_type, SettingType.CHANNEL)

        return ChannelSetting(bot, name_human, setting, permissions)

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        text_channels = []

        if not self.has_permission(ctx.interaction.user):
            return text_channels

        for channel in await ctx.interaction.guild.fetch_channels():
            if not isinstance(channel, discord.TextChannel):
                continue

            if ctx.value.lower() not in channel.name.lower():
                continue

            label = f"#{channel.name}"

            if self.value is not None and self.value.id == channel.id:
                label += ' (current)'

            text_channels.append(OptionChoice(label, str(channel.id)))

        return text_channels
