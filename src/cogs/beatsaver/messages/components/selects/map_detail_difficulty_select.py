from typing import List, Optional

import discord.ui
import pybeatsaver

from src.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from ..beatsaver_component import BeatSaverComponent
from ....storage.model.beatmap import Beatmap
from ....storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailDifficultySelect(BeatSaverComponent, discord.ui.Select):
    def __init__(self, bot: Kiyomi, parent, beatmap: Beatmap):
        BeatSaverComponent.__init__(self, bot, parent, beatmap)
        discord.ui.Select.__init__(
            self,
            custom_id=f"map:detail:difficulty:select:beatmap:{beatmap.id}",
            placeholder="Choose your favourite difficulty...",
            min_values=1,
            max_values=1,
            options=self.get_options(),
        )

    def get_options(self) -> List[discord.SelectOption]:
        options = []

        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            if beatmap_difficulty.characteristic is not self.parent.beatmap_characteristic:
                continue

            options.append(self.get_option(beatmap_difficulty))

        return options

    def get_option(self, beatmap_difficulty: BeatmapVersionDifficulty) -> discord.SelectOption:
        return discord.SelectOption(
            label=f"{beatmap_difficulty.difficulty_text}",
            description=self.difficulty_stars(beatmap_difficulty),
            value=f"{beatmap_difficulty.difficulty.serialize}",
            emoji=BeatSaverUtils.difficulty_to_emoji(self.bot, self.parent.guild, beatmap_difficulty.difficulty),
            default=self.parent.beatmap_difficulty == beatmap_difficulty.difficulty
        )

    async def callback(self, interaction: discord.Interaction):
        beatmap_difficulty = pybeatsaver.EDifficulty.deserialize(self.values[0])

        self.parent.beatmap_difficulty = beatmap_difficulty

        await self.parent.update()

    @staticmethod
    def difficulty_stars(beatmap_difficulty: BeatmapVersionDifficulty) -> Optional[str]:
        if beatmap_difficulty.stars is None:
            return None

        return f"{beatmap_difficulty.stars}★"
