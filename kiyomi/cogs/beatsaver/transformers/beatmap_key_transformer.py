from typing import Union, List, Optional

from discord import Interaction
from discord.app_commands import Transformer, Choice
from discord.ext.commands import Context

from ..beatsaver_api import BeatSaverAPI
from ..storage.model.beatmap import Beatmap


class BeatmapKeyTransformer(Transformer):
    async def transform(self, interaction: Interaction, value: str) -> Optional[Beatmap]:
        return await self.get_beatmap_by_key(interaction, value)

    async def autocomplete(
            self, interaction: Interaction, value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        beatmap = await self.get_beatmap_by_key(interaction, value)

        if beatmap is not None:
            return [Choice(name=beatmap.name, value=beatmap.id)]

        return []

    @staticmethod
    async def get_beatmap_by_key(interaction: Interaction, key: str) -> Optional[Beatmap]:
        if not key:
            return None

        ctx = await Context.from_interaction(interaction)

        async with ctx.bot.get_cog_api(BeatSaverAPI) as beatsaver:
            return await beatsaver.get_beatmap_by_key(key)
