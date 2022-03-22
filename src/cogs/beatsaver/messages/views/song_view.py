from typing import Union, Optional, Callable

import discord
import pybeatsaver
from discord import Embed, ApplicationContext

from src.cogs.beatsaver.messages.components.buttons.guild_leaderboard_button import GuildLeaderboardButton
from src.cogs.beatsaver.messages.components.buttons.map_details_button import MapDetailsButton
from src.cogs.beatsaver.messages.components.buttons.map_preview_button import MapPreviewButton
from src.cogs.beatsaver.messages.components.selects.map_detail_difficulty_select import MapDetailDifficultySelect
from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi

from src.kiyomi.base_view import BaseView


class SongView(BaseView):

    def __init__(self, bot: Kiyomi, beatmap: Beatmap):
        super().__init__(bot)

        self.bot = bot
        self.beatmap = beatmap

        self.embed: Callable[..., Embed] = self.default_embed

        self._beatmap_difficulty: Optional[pybeatsaver.Difficulty] = None
        self.message: Union[discord.Message, discord.WebhookMessage, None] = None

        self.update_buttons()

    @property
    def beatmap_difficulty(self) -> Optional[pybeatsaver.Difficulty]:
        if self._beatmap_difficulty is None:
            return self.beatmap.latest_version.difficulties[-1].difficulty

        return self._beatmap_difficulty

    @beatmap_difficulty.setter
    def beatmap_difficulty(self, beatmap_difficulty: pybeatsaver.Difficulty):
        self._beatmap_difficulty = beatmap_difficulty

    async def update(self) -> discord.Message:
        await self.update_buttons()

        return await self.message.edit(
            embed=self.embed(),
            view=self,
        )

    async def update_buttons(self):

        self.clear_items()

        map_details_button = MapDetailsButton(self.bot, self, self.beatmap)
        map_details_button.parent = self
        self.add_item(map_details_button)

        guild_leaderboard_button = GuildLeaderboardButton(self.bot, self, self.beatmap)
        guild_leaderboard_button.parent = self
        self.add_item(guild_leaderboard_button)

        preview_map = MapPreviewButton(self.bot, self, self.beatmap)
        preview_map.parent = self
        self.add_item(preview_map)

        self.difficulty_select = MapDetailDifficultySelect(self.bot, self, self.beatmap)
        self.difficulty_select.parent = self
        self.add_item(self.difficulty_select)

    async def send(self, ctx: ApplicationContext, target: Optional[discord.abc.Messageable] = None):
        if not isinstance(ctx, ApplicationContext):
            raise TypeError(f"expected Context not {ctx.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if target:
            ctx = target

        if self.embed is None:
            self.embed = self.default_embed

        self.message = await ctx.send(
            embed=self.embed(),
            view=self,
        )

        return self.message
