from typing import List, Optional

import discord.ui
import pybeatsaver
from discord import Emoji

from src.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.storage import Beatmap, BeatmapVersionDifficulty
from src.cogs.settings import SettingsAPI
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

    def get_options(self) -> List[discord.SelectOption]:
        options = []
        characteristics = []

        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            if beatmap_difficulty.characteristic not in characteristics:
                characteristics.append(beatmap_difficulty.characteristic)
                options.append(self.get_option(beatmap_difficulty))

        return options

    def get_option(self, beatmap_difficulty: BeatmapVersionDifficulty) -> discord.SelectOption:
        return discord.SelectOption(
            label=f"{beatmap_difficulty.characteristic_text}",
            value=f"{beatmap_difficulty.characteristic.serialize}",
            emoji=BeatSaverUtils.characteristic_to_emoji(self.bot, self.parent.guild, beatmap_difficulty.characteristic),
            default=self.parent.beatmap_characteristic == beatmap_difficulty.characteristic
        )

    async def callback(self, interaction: discord.Interaction):
        beatmap_characteristic = pybeatsaver.ECharacteristic.deserialize(self.values[0])

        self.parent.beatmap_characteristic = beatmap_characteristic

        await self.parent.update()
