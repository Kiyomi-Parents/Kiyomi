import discord
from discord import Permissions, app_commands, Interaction, AppCommandType
from discord.app_commands import Transform, CommandInvokeError
from discord.ext import commands

from kiyomi.cogs.settings import SettingsAPI
from kiyomi.cogs.settings.storage.model.toggle_setting import ToggleSetting
from .services import ServiceUnitOfWork
from .errors import NotFound
from .transformers.available_emoji_transformer import AvailableEmojiTransformer
from .transformers.enabled_emoji_transformer import EnabledEmojiTransformer
from kiyomi import permissions, Kiyomi, BaseCog


class EmojiEcho(BaseCog[ServiceUnitOfWork]):
    def __init__(self, bot: Kiyomi, service_uow: ServiceUnitOfWork):
        super().__init__(bot, service_uow)

        # Workaround until @app_commands.context_menu() supports self in function parameters
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Random Reaction",
                callback=self.random_reaction,
                type=AppCommandType.message,
            )
        )

    def register_events(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ToggleSetting.create(
                self.__cog_name__,
                "Let Kiyomi repost enabled emojis",
                "repost_emoji",
                Permissions(manage_messages=True),
            )
        ]

        self.bot.events.emit("setting_register", settings)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Repost emoji if enabled"""

        if msg.guild is None:
            return

        if msg.author.id == self.bot.user.id:
            return

        async with self.bot.get_cog_api(SettingsAPI) as settings:
            if await settings.get(msg.guild.id, "repost_emoji"):
                emoji = await self.service_uow.echo_emojis.get_emoji_from_message(msg.guild.id, msg.content)

                if emoji is not None:
                    await msg.channel.send(emoji)

    emoji = app_commands.Group(
        name="emoji",
        description="Emojis that Kiyomi is allowed to play with",
    )

    # @app_commands.context_menu(name="Random Reaction")
    async def random_reaction(self, ctx: Interaction, message: discord.Message):
        emoji = await self.service_uow.echo_emojis.get_random_enabled_emoji()

        await ctx.response.send_message("give me a sec", ephemeral=True)
        await ctx.delete_original_message()

        await message.add_reaction(emoji)

    @app_commands.command(name="emoji-random")
    async def emoji_random(self, ctx: Interaction):
        """Posts a random enabled emoji"""
        emoji = await self.service_uow.echo_emojis.get_random_enabled_emoji()

        await ctx.response.send_message("give me a sec", ephemeral=True)
        await ctx.delete_original_message()

        await ctx.channel.send(str(emoji))

    # @random_reaction.error
    @emoji_random.error
    async def emoji_random_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, NotFound):
            return await error.handle(ctx=ctx, message=f"You don't seem to have any emojis enabled...")

    @emoji.command(name="enable")
    @app_commands.describe(emoji="Choose an emoji")
    @permissions.is_bot_owner()
    async def emoji_enable(
        self,
        ctx: Interaction,
        emoji: Transform[discord.Emoji, AvailableEmojiTransformer],
    ):
        """Allow the given emoji to be used by the bot"""
        await ctx.response.defer(ephemeral=True)

        await self.service_uow.echo_emojis.enable_emoji(emoji.guild_id, emoji.id, emoji.name)
        await self.service_uow.save_changes()

        await ctx.followup.send(f"Enabled {str(emoji)}", ephemeral=True)

    @emoji.command(name="disable")
    @app_commands.describe(emoji="Choose an emoji")
    @permissions.is_bot_owner()
    async def emoji_disable(self, ctx: Interaction, emoji: Transform[discord.Emoji, EnabledEmojiTransformer]):
        """Disallow the given emoji from being used by the bot"""
        await ctx.response.defer(ephemeral=True)

        await self.service_uow.echo_emojis.disable_emoji(emoji.id)
        await self.service_uow.save_changes()

        await ctx.followup.send(f"Disabled {str(emoji)}", ephemeral=True)
