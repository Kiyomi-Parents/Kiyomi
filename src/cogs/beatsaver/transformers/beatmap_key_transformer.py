from typing import Union, List, Optional

from discord import Interaction
from discord.app_commands import Transformer, Choice
from discord.ext.commands import Context

from ..beatsaver_api import BeatSaverAPI
from ..storage.model.beatmap import Beatmap


class BeatmapKeyTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> Optional[Beatmap]:
        return await cls.get_beatmap_by_key(interaction, value)

    @classmethod
    async def autocomplete(
            cls,
            interaction: Interaction,
            value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        beatmap = await cls.get_beatmap_by_key(interaction, value)

        if beatmap is not None:
            return [Choice(name=beatmap.name, value=beatmap.id)]

        return []

    @staticmethod
    async def get_beatmap_by_key(interaction: Interaction, key: str) -> Optional[Beatmap]:
        if not key:
            return None

        ctx = await Context.from_interaction(interaction)

        beatsaver = ctx.bot.get_cog_api(BeatSaverAPI)
        return await beatsaver.beatmap_service.get_beatmap_by_key(key)