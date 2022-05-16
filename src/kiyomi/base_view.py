from abc import ABC, abstractmethod
from typing import Optional, Union, Callable, Awaitable, Any

import discord
from discord import Guild, Interaction
from discord.ext.commands import Context
from discord.ui import Item

from .base_embed import BaseEmbed
from .kiyomi import Kiyomi


class BaseView(discord.ui.View, ABC):

    def __init__(self, bot: Kiyomi, guild: Guild):
        super().__init__(timeout=None)

        self.bot = bot
        self.guild = guild

        self.embed: Optional[Callable[[], Awaitable[BaseEmbed]]] = None
        self.message: Union[discord.Message, discord.WebhookMessage, None] = None

        self.update_buttons()

    async def get_current_embed(self) -> Optional[BaseEmbed]:
        if self.embed is None:
            default_embed = self.default_embed()

            if default_embed is not None:
                embed = await default_embed()
                await embed.after_init()
                return embed

        if self.embed is not None:
            embed = await self.embed()
            await embed.after_init()
            return embed

        return None

    def default_embed(self) -> Optional[Callable[[], Awaitable[BaseEmbed]]]:
        for child in self.children:
            get_embed = getattr(child, "get_embed", None)

            if callable(get_embed):
                if isinstance(child, discord.ui.Button):
                    self.disabled_clicked_button(child)

                return get_embed
        # TODO: error embed

    async def update(
            self,
            interaction: discord.Interaction,
            button_clicked: Optional[discord.ui.Button] = None
    ) -> discord.Message:
        if self.message is None:
            self.message = interaction.message

        self.clear_items()
        self.update_buttons()
        await self.run_component_after_init()

        if button_clicked is not None:
            self.disabled_clicked_button(button_clicked)

        return await self.message.edit(
                embed=await self.get_current_embed(),
                view=self,
        )

    def disabled_clicked_button(self, button_clicked: discord.ui.Button):
        for child in self.children:
            if isinstance(child, button_clicked.__class__):
                if child.custom_id == button_clicked.custom_id:
                    child.disabled = True

    @abstractmethod
    def update_buttons(self):
        raise NotImplementedError("Derived classes need to implement this.")

    async def run_component_after_init(self):
        from .base_component import BaseComponent  # Avoiding circular import

        for child in self.children:
            if isinstance(child, BaseComponent):
                await child.after_init()

    async def send(
            self,
            ctx: Optional[Context] = None,
            target: Optional[discord.abc.Messageable] = None
    ) -> discord.Message:
        if ctx is not None and not isinstance(ctx, Context):
            raise TypeError(f"expected Context not {ctx.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if ctx is None and target is None:
            raise RuntimeError("ctx and target were not provided")

        if target:
            ctx = target

        await self.run_component_after_init()

        self.message = await ctx.send(
                embed=await self.get_current_embed(),
                view=self,
        )

        return self.message

    async def respond(
            self,
            interaction: discord.Interaction,
            target: Optional[discord.abc.Messageable] = None
    ) -> Union[discord.Message, discord.InteractionMessage, discord.WebhookMessage]:
        if not isinstance(interaction, discord.Interaction):
            raise TypeError(f"expected Interaction not {interaction.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        await self.run_component_after_init()

        if target:
            self.message = await target.send(
                    embed=await self.get_current_embed(),
                    view=self
            )
        else:
            if interaction.response.is_done():
                msg = await interaction.followup.send(
                        embed=await self.get_current_embed(),
                        view=self
                )
                # convert from WebhookMessage to Message reference to bypass 15min webhook token timeout
                msg = await msg.channel.fetch_message(msg.id)
            else:
                await interaction.response.send_message(
                        embed=await self.get_current_embed(),
                        view=self
                )

                msg = await interaction.original_message()

            if isinstance(msg, discord.WebhookMessage):
                self.message = await msg.channel.fetch_message(msg.id)
            elif isinstance(msg, discord.Message):
                self.message = msg
            elif isinstance(msg, discord.Interaction):
                self.message = await msg.original_message()

        return self.message

    # TODO: Add error handling for views
    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Any]) -> None:
        await super(BaseView, self).on_error(interaction, error, item)
