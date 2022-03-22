import discord
import pybeatsaver

from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi


class MapPreviewButton(discord.ui.Button):
    def __init__(self, bot: Kiyomi, beatmap: Beatmap):
        self.bot = bot
        self.beatmap = beatmap
        self.difficulty: pybeatsaver.Difficulty = None

        super().__init__(
            label="Map Preview",
            style=discord.enums.ButtonStyle.primary,
            url=self.preview_url
        )

    async def update(self, interaction, difficulty: pybeatsaver.Difficulty):
        self.difficulty = difficulty
        self._underlying.url = self.preview_url
        # TODO: Figure out how to make the button actually update

    @property
    def preview_url(self) -> str:
        result = f"https://skystudioapps.com/bs-viewer/?id={self.beatmap.id}"
        if self.difficulty is not None:
            result += f"&difficulty={self.difficulty_index}"
        return result

    @property
    def difficulty_index(self):
        difficulties = [bmv_diff.difficulty.value for bmv_diff in self.beatmap.difficulties]
        if self.difficulty.value in difficulties:
            return difficulties.index(self.difficulty.value)
        return 69  # The preview website will just take the max diff if the given index is higher than the max.
