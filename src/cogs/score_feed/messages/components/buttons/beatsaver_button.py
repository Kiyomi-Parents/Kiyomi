import discord

from src.cogs.score_feed.messages.components.score_feed_component import ScoreFeedComponent
from src.kiyomi import Kiyomi


class BeatSaverButton(ScoreFeedComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent, beatmap_id: str):
        self.beatmap_id = beatmap_id

        ScoreFeedComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            label="Beat Saver",
            style=discord.enums.ButtonStyle.primary,
            url=self.preview_url
        )

    @property
    def preview_url(self) -> str:
        return f"https://beatsaver.com/maps/{self.beatmap_id}"
