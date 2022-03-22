from typing import List, Optional

import discord.ui
import pybeatsaver
from discord import Emoji

from src.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.storage import Beatmap, BeatmapVersionDifficulty
from src.cogs.settings import SettingsAPI
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
            options.append(self.get_option(beatmap_difficulty))

        return options

    def get_option(self, beatmap_difficulty: BeatmapVersionDifficulty) -> discord.SelectOption:
        return discord.SelectOption(
            label=f"{beatmap_difficulty.difficulty_text}",
            description=self.difficulty_stars(beatmap_difficulty),
            value=f"{beatmap_difficulty.difficulty.value}",
            emoji=BeatSaverUtils.difficulty_to_emoji(self.bot, self.parent.guild, beatmap_difficulty.difficulty),
            default=self.parent.beatmap_difficulty == beatmap_difficulty.difficulty
        )

    async def callback(self, interaction: discord.Interaction):
        beatmap_difficulty = pybeatsaver.Difficulty(self.values[0])

        self.parent.beatmap_difficulty = beatmap_difficulty

        await self.parent.update()

    @property
    def selected_difficulty(self) -> pybeatsaver.Difficulty:
        if len(self.values) > 0:
            return pybeatsaver.Difficulty(self.values[0])

    @staticmethod
    def difficulty_stars(beatmap_difficulty: BeatmapVersionDifficulty) -> Optional[str]:
        if beatmap_difficulty.stars is None:
            return None

        return f"{beatmap_difficulty.stars}★"
