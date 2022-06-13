from typing import Union, List

from discord import Interaction
from discord.app_commands import Transformer, Choice
from discord.ext.commands import Context

from ..settings_api import SettingsAPI
from ..errors import PermissionDenied
from src.kiyomi import Utils


class SettingNameTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> str:
        ctx = await Context.from_interaction(interaction)
        settings_api = ctx.bot.get_cog_api(SettingsAPI)

        if not settings_api.has_permission(value, interaction.user):
            raise PermissionDenied(value)

        return value

    @classmethod
    async def autocomplete(
        cls, interaction: Interaction, value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        ctx = await Context.from_interaction(interaction)
        settings_api = ctx.bot.get_cog_api(SettingsAPI)

        settings = []

        for setting in settings_api.get_registered():

            if not setting.has_permission(interaction.user):
                continue

            if value.isspace() or not setting.name_human.startswith(value.lower()):
                continue

            settings.append(Choice(name=setting.name_human, value=setting.name))

        return Utils.limit_list(settings, 25)
