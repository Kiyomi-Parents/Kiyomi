from typing import List, Optional

import discord.ui
import pybeatsaver
from discord import Emoji

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
            value=f"{beatmap_difficulty.difficulty.value}",
            emoji=self.difficulty_to_emoji(beatmap_difficulty.difficulty),
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

    def difficulty_to_emoji(self, difficulty: pybeatsaver.Difficulty) -> Optional[Emoji]:
        if self.parent.guild is None:
            return None

        settings = self.bot.get_cog_api(SettingsAPI)

        if difficulty == pybeatsaver.Difficulty.EASY:
            return settings.get(self.parent.guild.id, "easy_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.NORMAL:
            return settings.get(self.parent.guild.id, "normal_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.HARD:
            return settings.get(self.parent.guild.id, "hard_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.EXPERT:
            return settings.get(self.parent.guild.id, "expert_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.EXPERT_PLUS:
            return settings.get(self.parent.guild.id, "expert_plus_difficulty_emoji")

        return None
