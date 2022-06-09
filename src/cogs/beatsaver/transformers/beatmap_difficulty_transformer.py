from typing import Union, List

import pybeatsaver
from discord import Interaction
from discord.app_commands import Transformer, Choice

from .beatmap_characteristic_transformer import BeatmapCharacteristicTransformer
from .beatmap_key_transformer import BeatmapKeyTransformer
from src.kiyomi import BadArgument


class BeatmapDifficultyTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> pybeatsaver.EDifficulty:
        if pybeatsaver.EDifficulty.has_value(value):
            return pybeatsaver.EDifficulty.deserialize(value)

        raise BadArgument(interaction, value)

    @classmethod
    async def autocomplete(
        cls, interaction: Interaction, value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        beatmap = await BeatmapKeyTransformer.transform(interaction, interaction.namespace.key)
        if beatmap is None:
            return []

        try:
            characteristic = await BeatmapCharacteristicTransformer.transform(interaction, interaction.namespace.game_mode)
        except BadArgument:
            characteristic = pybeatsaver.ECharacteristic.STANDARD

        beatmap_difficulties = []

        for beatmap_difficulty in beatmap.difficulties:
            if beatmap_difficulty.characteristic is not characteristic:
                continue

            beatmap_difficulties.append(
                Choice(
                    name=beatmap_difficulty.difficulty_text,
                    value=beatmap_difficulty.difficulty.serialize,
                )
            )

        return beatmap_difficulties
