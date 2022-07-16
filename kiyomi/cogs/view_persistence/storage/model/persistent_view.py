from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union, TYPE_CHECKING

import discord
from discord.ext.commands import Context

from kiyomi import Kiyomi
from kiyomi.base_view import BaseView

if TYPE_CHECKING:
    from .persistence import Persistence


class PersistentView(BaseView, ABC):
    @abstractmethod
    async def serialize_persistence(self) -> "Persistence":
        pass

    @staticmethod
    @abstractmethod
    async def deserialize_persistence(bot: Kiyomi, persistence: "Persistence") -> PersistentView:
        pass

    async def send(
        self,
        ctx: Optional[Context] = None,
        target: Optional[discord.abc.Messageable] = None,
    ) -> discord.Message:
        message = await super(PersistentView, self).send(ctx, target)

        self.bot.events.emit("on_new_view_sent", await self.serialize_persistence())

        return message

    async def respond(
        self,
        interaction: discord.Interaction,
        target: Optional[discord.abc.Messageable] = None,
    ) -> Union[discord.Message, discord.WebhookMessage]:
        message = await super(PersistentView, self).respond(interaction, target)

        self.bot.events.emit("on_new_view_sent", await self.serialize_persistence())

        return message
