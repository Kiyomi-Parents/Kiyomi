from typing import Union, Optional, Callable

import discord
import pybeatsaver
from discord import Embed, Guild
from discord.ext.commands import Context

from ..components.buttons.guild_leaderboard_button import GuildLeaderboardButton
from ..components.buttons.map_details_button import MapDetailsButton
from ..components.buttons.map_preview_button import MapPreviewButton
from ..components.selects.map_detail_difficulty_select import MapDetailDifficultySelect
from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi

from src.kiyomi.base_view import BaseView


# TODO:
# Need to save the view type and the message id to the database, for it to be truly persistent.
# When the bot restarts we need to attach all the attach all the views to the messages IDs in Kiyomi class (add_view)
# This could probably be a new cog?
class SongView(BaseView):

    def __init__(self, bot: Kiyomi, guild: Guild, beatmap: Beatmap):
        super().__init__(bot, guild)

        self.beatmap = beatmap

        self._beatmap_difficulty: Optional[pybeatsaver.Difficulty] = None
        self.message: Union[discord.Message, discord.WebhookMessage, None] = None

        self.update_buttons()

        self.embed: Callable[[], Embed] = self.default_embed

    @property
    def beatmap_difficulty(self) -> Optional[pybeatsaver.Difficulty]:
        if self._beatmap_difficulty is None:
            return self.beatmap.latest_version.difficulties[-1].difficulty

        return self._beatmap_difficulty

    @beatmap_difficulty.setter
    def beatmap_difficulty(self, beatmap_difficulty: pybeatsaver.Difficulty):
        self._beatmap_difficulty = beatmap_difficulty

    async def update(self) -> discord.Message:
        self.update_buttons()

        return await self.message.edit(
            embed=self.embed(),
            view=self,
        )

    def update_buttons(self):
        self.clear_items()

        self.add_item(MapDetailsButton(self.bot, self, self.beatmap))
        self.add_item(GuildLeaderboardButton(self.bot, self, self.beatmap))
        self.add_item(MapPreviewButton(self.bot, self, self.beatmap))
        self.add_item(MapDetailDifficultySelect(self.bot, self, self.beatmap))

    async def send(self, ctx: Context, target: Optional[discord.abc.Messageable] = None) -> discord.Message:
        if not isinstance(ctx, Context):
            raise TypeError(f"expected Context not {ctx.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if target:
            ctx = target

        self.message = await ctx.send(
            embed=self.embed(),
            view=self,
        )

        return self.message

    async def respond(self, interaction: discord.Interaction, target: Optional[discord.abc.Messageable] = None) -> Union[discord.Message, discord.WebhookMessage]:
        if not isinstance(interaction, discord.Interaction):
            raise TypeError(f"expected Interaction not {interaction.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if target:
            self.message = await target.send(
                embed=self.embed(),
                view=self
            )
        else:
            if interaction.response.is_done():
                msg = await interaction.followup.send(
                    embed=self.embed(),
                    view=self
                )
                # convert from WebhookMessage to Message reference to bypass 15min webhook token timeout
                msg = await msg.channel.fetch_message(msg.id)
            else:
                msg = await interaction.response.send_message(
                    embed=self.embed(),
                    view=self
                )

            if isinstance(msg, discord.WebhookMessage):
                self.message = await msg.channel.fetch_message(msg.id)
            elif isinstance(msg, discord.Message):
                self.message = msg
            elif isinstance(msg, discord.Interaction):
                self.message = await msg.original_message()

        return self.message
