from typing import Union, List

from discord import Interaction
from discord.app_commands import Transformer, Choice
from discord.ext.commands import Context

from ..settings_api import SettingsAPI
from ..errors import SettingsCogException
from .setting_name_transformer import SettingNameTransformer
from src.kiyomi import Utils


class SettingValueTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> str:
        ctx = await Context.from_interaction(interaction)
        settings_api = ctx.bot.get_cog_api(SettingsAPI)

        setting = await SettingNameTransformer.transform(interaction, interaction.namespace.setting)
        await settings_api.setting_service.validate_setting_value(interaction.guild_id, setting, value)

        return value

    @classmethod
    async def autocomplete(
        cls, interaction: Interaction, value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        ctx = await Context.from_interaction(interaction)
        settings_api = ctx.bot.get_cog_api(SettingsAPI)

        setting_name = await SettingNameTransformer.transform(interaction, interaction.namespace.setting)

        try:
            setting = await settings_api.setting_service.get(interaction.guild_id, setting_name)
        except SettingsCogException:
            return []

        if setting is None:
            return []

        if not setting.has_permission(interaction.user):
            return []

        values = await setting.get_autocomplete(interaction, value)

        return Utils.limit_list(values, 25)
