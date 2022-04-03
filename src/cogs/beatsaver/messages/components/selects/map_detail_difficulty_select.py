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

    async def after_init(self):
        self.options = await self.get_options_async()

    def get_beatmap_difficulties(self) -> List[BeatmapVersionDifficulty]:
        beatmap_difficulties = []

        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            if beatmap_difficulty.characteristic is not self.parent.beatmap_characteristic:
                continue

            beatmap_difficulties.append(beatmap_difficulty)

        return beatmap_difficulties

    def get_options(self) -> List[discord.SelectOption]:
        return [discord.SelectOption(
            label=f"{beatmap_difficulty.difficulty_text}",
            description=self.difficulty_stars(beatmap_difficulty),
            value=f"{beatmap_difficulty.difficulty.serialize}",
            default=self.parent.beatmap_difficulty == beatmap_difficulty.difficulty
        ) for beatmap_difficulty in self.get_beatmap_difficulties()]

    async def get_options_async(self) -> List[discord.SelectOption]:
        options = []

        for beatmap_difficulty in self.get_beatmap_difficulties():
            difficulty_emoji = await BeatSaverUtils.difficulty_to_emoji(self.bot, self.parent.guild, beatmap_difficulty.difficulty)

            options.append(discord.SelectOption(
                label=f"{beatmap_difficulty.difficulty_text}",
                description=self.difficulty_stars(beatmap_difficulty),
                value=f"{beatmap_difficulty.difficulty.serialize}",
                emoji=difficulty_emoji,
                default=self.parent.beatmap_difficulty == beatmap_difficulty.difficulty
            ))

        return options

    async def callback(self, interaction: discord.Interaction):
        beatmap_difficulty = pybeatsaver.EDifficulty.deserialize(self.values[0])

        self.parent.beatmap_difficulty = beatmap_difficulty

        await self.parent.update(interaction)

    @staticmethod
    def difficulty_stars(beatmap_difficulty: BeatmapVersionDifficulty) -> Optional[str]:
        if beatmap_difficulty.stars is None:
            return None

        return f"{beatmap_difficulty.stars}★"
