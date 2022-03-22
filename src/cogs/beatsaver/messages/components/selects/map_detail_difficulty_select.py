from typing import List, Callable

import asyncio
import discord.ui
import pybeatsaver
from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.storage import Beatmap, BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailDifficultySelect(BeatSaverComponent, discord.ui.Select):
    def __init__(self, bot: Kiyomi, beatmap: Beatmap, events: AsyncIOEventEmitter, update_funcs: List[Callable]):
        BeatSaverComponent.__init__(self, bot, events, beatmap)
        discord.ui.Select.__init__(
            self,
            placeholder="Choose your favourite difficulty...",
            min_values=1,
            max_values=1,
            options=self.get_options(),
        )
        self.update_funcs = update_funcs

    def get_options(self) -> List[discord.SelectOption]:
        options = []

        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            options.append(self.get_option(beatmap_difficulty))

        return options

    def get_option(self, beatmap_difficulty: BeatmapVersionDifficulty) -> discord.SelectOption:
        return discord.SelectOption(
            label=f"{beatmap_difficulty.difficulty_text}",
            value=f"{beatmap_difficulty.difficulty.value}",
            emoji="🟥"  # TODO: Add emoji here
        )

    async def callback(self, interaction: discord.Interaction):
        for func in self.update_funcs:
            if asyncio.iscoroutinefunction(func):
                await func(interaction, pybeatsaver.Difficulty(self.values[0]))
