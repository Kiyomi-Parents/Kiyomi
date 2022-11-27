from typing import Generic, TypeVar

import discord

from kiyomi.base_component import BaseComponent
from kiyomi.base_view import BaseView
from kiyomi import Kiyomi

T = TypeVar("T", bound=BaseView)


class BeatSaverButton(BaseComponent[T], discord.ui.Button, Generic[T]):
    def __init__(self, bot: Kiyomi, parent, beatmap_id: str):
        self.beatmap_id = beatmap_id

        BaseComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            label="Beat Saver",
            style=discord.enums.ButtonStyle.primary,
            url=self.preview_url,
        )

    async def after_init(self):
        async with self.bot.get_cog("SettingsAPI") as settings:
            emoji = await settings.get_override_or_default(self.parent.guild.id, "beatsaver_emoji")

        if emoji:
            self.label = None
            self.emoji = emoji

    @property
    def preview_url(self) -> str:
        return f"https://beatsaver.com/maps/{self.beatmap_id}"
