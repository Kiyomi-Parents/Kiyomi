from typing import Union, List

import pybeatsaver
from discord import Interaction
from discord.app_commands import Transformer, Choice

from .beatmap_key_transformer import BeatmapKeyTransformer
from kiyomi import BadArgument


class BeatmapCharacteristicTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> pybeatsaver.ECharacteristic:
        if pybeatsaver.ECharacteristic.has_value(value):
            return pybeatsaver.ECharacteristic.deserialize(value)

        raise BadArgument(interaction, value)

    @classmethod
    async def autocomplete(
        cls, interaction: Interaction, value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        beatmap = await BeatmapKeyTransformer.transform(interaction, interaction.namespace.key)
        if beatmap is None:
            return []

        beatmap_characteristics = []
        characteristics = []

        for beatmap_difficulty in beatmap.difficulties:
            if beatmap_difficulty.characteristic in characteristics:
                continue

            beatmap_characteristics.append(
                Choice(
                    name=beatmap_difficulty.characteristic_text,
                    value=beatmap_difficulty.characteristic.serialize,
                )
            )
            characteristics.append(beatmap_difficulty.characteristic)

        return beatmap_characteristics
