import discord

from src.kiyomi import Kiyomi


class MapPreviewButton(discord.ui.Button):
    def __init__(self, bot: Kiyomi, beatmap_id: str):
        self.bot = bot
        self.beatmap_id = beatmap_id

        super().__init__(
            label="Map Preview",
            style=discord.enums.ButtonStyle.primary,
            url=self.preview_url
        )

    @property
    def preview_url(self) -> str:
        return f"https://skystudioapps.com/bs-viewer/?id={self.beatmap_id}"
