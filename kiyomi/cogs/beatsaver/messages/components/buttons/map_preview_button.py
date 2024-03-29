import discord

from kiyomi.cogs.beatsaver.storage.model.beatmap import Beatmap
from ..beatsaver_component import BeatSaverComponent
from kiyomi import Kiyomi


class MapPreviewButton(BeatSaverComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent, beatmap: Beatmap):
        BeatSaverComponent.__init__(self, bot, parent, beatmap)
        discord.ui.Button.__init__(
            self,
            label="Map Preview",
            style=discord.enums.ButtonStyle.primary,
            url=self.preview_url,
        )

    async def after_init(self):
        async with self.bot.get_cog("SettingsAPI") as settings:
            emoji = await settings.get_override_or_default(self.parent.guild.id, "map_preview_emoji")

        if emoji:
            self.label = None
            self.emoji = emoji

    @property
    def preview_url(self) -> str:
        result = f"https://skystudioapps.com/bs-viewer/?id={self.beatmap.id}"

        if self.parent is not None:
            result += f"&difficulty={self.difficulty_index}"

        return result

    @property
    def difficulty_index(self):
        difficulties = [bmv_diff.difficulty.value for bmv_diff in self.beatmap.difficulties]

        if self.parent.beatmap_difficulty.value in difficulties:
            return difficulties.index(self.parent.beatmap_difficulty.value)

        return 69  # The preview website will just take the max diff if the given index is higher than the max.
