from typing import Union, List

from discord import Interaction
from discord.app_commands import Transformer, Choice
from discord.ext.commands import Context

from ..settings_api import SettingsAPI
from ..errors import PermissionDenied
from kiyomi import Utils


class SettingNameTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> str:
        ctx = await Context.from_interaction(interaction)

        async with ctx.bot.get_cog_api(SettingsAPI) as settings_api:
            if not settings_api.has_permission(value, interaction.user):
                raise PermissionDenied(value)

        return value

    @classmethod
    async def autocomplete(
        cls, interaction: Interaction, value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        ctx = await Context.from_interaction(interaction)
        settings = []

        async with ctx.bot.get_cog_api(SettingsAPI) as settings_api:
            for setting in settings_api.get_registered():

                if not setting.has_permission(interaction.user):
                    continue

                if value.isspace() or not setting.name_human.startswith(value.lower()):
                    continue

                choice_name = f"[{setting.group}] {setting.name_human}"
                abstract_setting = await settings_api.get_setting(interaction.guild_id, setting.name)

                if abstract_setting and abstract_setting.value:
                    choice_name += f" [{abstract_setting.value_human}]"

                settings.append(Choice(name=choice_name, value=setting.name))

        return Utils.limit_list(settings, 25)
