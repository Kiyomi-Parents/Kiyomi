from __future__ import annotations

from typing import Generic, TypeVar, TYPE_CHECKING

import discord

from kiyomi.base_component import BaseComponent
from kiyomi.base_view import BaseView
from kiyomi import Kiyomi

if TYPE_CHECKING:
    from kiyomi.cogs.settings import SettingsAPI

T = TypeVar("T", bound=BaseView)


class InviteButton(BaseComponent[T], discord.ui.Button, Generic[T]):
    def __init__(self, bot: Kiyomi, parent):
        BaseComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            label="Invite Kiyomi",
            style=discord.enums.ButtonStyle.primary,
            url=bot.invite_url,
        )

    async def after_init(self):
        settings: "SettingsAPI" = self.bot.get_cog("SettingsAPI")

        self.emoji = await settings.get_override_or_default(self.parent.guild.id, "invite_button_emoji")
