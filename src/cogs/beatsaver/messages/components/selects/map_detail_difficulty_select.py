from typing import List

import asyncio
import discord.ui
import pybeatsaver
from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.storage import Beatmap, BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailDifficultySelect(BeatSaverComponent, discord.ui.Select):
    def __init__(self, bot: Kiyomi, beatmap: Beatmap, events: AsyncIOEventEmitter):
        BeatSaverComponent.__init__(self, bot, events, beatmap)

        # options = [
        #     discord.SelectOption(label="Red", value="", description="Your favourite colour is red", emoji="🟥", default=True),
        #     discord.SelectOption(label="Green", value="", description="Your favourite colour is green", emoji="🟩"),
        #     discord.SelectOption(label="Blue", value="", description="Your favourite colour is blue", emoji="🟦"),
        # ]

        discord.ui.Select.__init__(self,
                                   placeholder="Choose your favourite difficulty...",
                                   min_values=1,
                                   max_values=1,
                                   options=self.get_options(),
                                   )

    def get_options(self) -> List[discord.SelectOption]:
        options = []

        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            options.append(self.get_option(beatmap_difficulty))

        options[0].default = True

        return options

    def get_option(self, beatmap_difficulty: BeatmapVersionDifficulty) -> discord.SelectOption:
        return discord.SelectOption(
            label=f"{beatmap_difficulty.difficulty_text}",
            value=f"{beatmap_difficulty.difficulty.value}",
            emoji="🟥"  # TODO: Add emoji here
        )

    async def callback(self, interaction: discord.Interaction):
        print("start before event")

        self.events.emit("on_difficulty_update", interaction, pybeatsaver.Difficulty(self.values[0]))
        await asyncio.sleep(10)
        print("start after event")
