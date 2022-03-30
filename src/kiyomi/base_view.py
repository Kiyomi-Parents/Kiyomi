from abc import ABC, abstractmethod
from typing import Optional, Union, Callable

import discord
from discord import Embed, Guild
from discord.ext.commands import Context

from .kiyomi import Kiyomi


class BaseView(discord.ui.View, ABC):
    def __init__(self, bot: Kiyomi, guild: Guild):
        super().__init__(timeout=None)

        self.bot = bot
        self.guild = guild

        self.embed: Callable[[], Embed] = self.default_embed
        self.message: Union[discord.Message, discord.WebhookMessage, None] = None

        self.update_buttons()

    def default_embed(self) -> Optional[Embed]:
        for child in self.children:
            get_embed = getattr(child, "get_embed", None)

            if callable(get_embed):
                if isinstance(child, discord.ui.Button):
                    self.disabled_clicked_button(child)

                return get_embed()
        # TODO: error embed

    async def update(self, button_clicked: Optional[discord.ui.Button] = None) -> discord.Message:
        self.clear_items()
        self.update_buttons()

        if button_clicked is not None:
            self.disabled_clicked_button(button_clicked)

        return await self.message.edit(
            embed=self.embed(),
            view=self,
        )

    def disabled_clicked_button(self, button_clicked: discord.ui.Button):
        for child in self.children:
            if isinstance(child, button_clicked.__class__):
                if child.custom_id == button_clicked.custom_id:
                    child.disabled = True

    @abstractmethod
    def update_buttons(self):
        pass

    async def send(self, ctx: Optional[Context] = None, target: Optional[discord.abc.Messageable] = None) -> discord.Message:
        if ctx is not None and not isinstance(ctx, Context):
            raise TypeError(f"expected Context not {ctx.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if ctx is None and target is None:
            raise RuntimeError("ctx and target were not provided")

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
