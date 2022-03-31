from typing import List

import discord.ui
import pybeatsaver

from ....beatsaver_utils import BeatSaverUtils
from ..beatsaver_component import BeatSaverComponent
from ....storage.model.beatmap import Beatmap
from ....storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailCharacteristicSelect(BeatSaverComponent, discord.ui.Select):
    def __init__(self, bot: Kiyomi, parent, beatmap: Beatmap):
        BeatSaverComponent.__init__(self, bot, parent, beatmap)
        discord.ui.Select.__init__(
            self,
            custom_id=f"map:detail:characteristic:select:beatmap:{beatmap.id}",
            placeholder="Choose your favourite game mode...",
            min_values=1,
            max_values=1,
            options=self.get_options(),
        )

    async def after_init(self):
        self.options = await self.get_options_async()

    def get_beatmap_difficulties(self) -> List[BeatmapVersionDifficulty]:
        beatmap_difficulties = []
        characteristics = []

        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            if beatmap_difficulty.characteristic not in characteristics:
                beatmap_difficulties.append(beatmap_difficulty)
                characteristics.append(beatmap_difficulty.characteristic)

        return beatmap_difficulties

    def get_options(self) -> List[discord.SelectOption]:
        return [discord.SelectOption(
            label=f"{beatmap_difficulty.characteristic_text}",
            value=f"{beatmap_difficulty.characteristic.serialize}",
            default=self.parent.beatmap_characteristic == beatmap_difficulty.characteristic
        ) for beatmap_difficulty in self.get_beatmap_difficulties()]

    async def get_options_async(self) -> List[discord.SelectOption]:
        options = []

        for beatmap_difficulty in self.get_beatmap_difficulties():
            characteristic_emoji = await BeatSaverUtils.characteristic_to_emoji(self.bot, self.parent.guild, beatmap_difficulty.characteristic)

            options.append(discord.SelectOption(
                label=f"{beatmap_difficulty.characteristic_text}",
                value=f"{beatmap_difficulty.characteristic.serialize}",
                emoji=characteristic_emoji,
                default=self.parent.beatmap_characteristic == beatmap_difficulty.characteristic
            ))

        return options

    async def callback(self, interaction: discord.Interaction):
        beatmap_characteristic = pybeatsaver.ECharacteristic.deserialize(self.values[0])

        self.parent.beatmap_characteristic = beatmap_characteristic

        await self.parent.update()
