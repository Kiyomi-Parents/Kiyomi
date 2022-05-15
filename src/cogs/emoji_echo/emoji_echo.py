import discord
from discord import Permissions, app_commands, Interaction, AppCommandType
from discord.app_commands import Transform, CommandInvokeError
from discord.ext import commands

from .services.emoji_service import EmojiService
from .emoji_echo_cog import EmojiEchoCog
from .errors import NotFound
from .transformers.available_emoji_transformer import AvailableEmojiTransformer
from .transformers.enabled_emoji_transformer import EnabledEmojiTransformer
from src.cogs.settings import SettingsAPI
from src.cogs.settings.storage import ToggleSetting
from src.kiyomi import permissions, Kiyomi


class EmojiEcho(EmojiEchoCog):

    def __init__(self, bot: Kiyomi, emoji_service: EmojiService):
        super().__init__(bot, emoji_service)

        # Workaround until @app_commands.context_menu() supports self in function parameters
        self.bot.tree.add_command(app_commands.ContextMenu(
                name="Random Reaction",
                callback=self.random_reaction,
                type=AppCommandType.message
        ))

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ToggleSetting.create("let Kiyomi repost enabled emojis", "repost_emoji", Permissions(manage_messages=True))
        ]

        self.bot.events.emit("setting_register", settings)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Repost emoji if enabled"""

        if msg.guild is None:
            return

        if msg.author.id == self.bot.user.id:
            return

        settings = self.bot.get_cog_api(SettingsAPI)

        if settings.get(msg.guild.id, "repost_emoji"):
            emoji = await self.emoji_service.get_emoji_from_message(msg.guild.id, msg.content)

            if emoji is not None:
                await msg.channel.send(emoji)

    emoji = app_commands.Group(
            name="emoji",
            description="Emojis that Kiyomi is allowed to play with",
    )

    # @app_commands.context_menu(name="Random Reaction")
    async def random_reaction(self, ctx: Interaction, message: discord.Message):
        emoji = await self.emoji_service.get_random_enabled_emoji()

        await ctx.response.defer()
        msg = await ctx.original_message()
        await msg.delete()

        await message.add_reaction(emoji)

    @app_commands.command(name="emoji-random")
    async def emoji_random(self, ctx: Interaction):
        """Posts a random enabled emoji"""
        emoji = await self.emoji_service.get_random_enabled_emoji()

        await ctx.response.defer()
        msg = await ctx.original_message()
        await msg.delete()

        await ctx.channel.send(str(emoji))

    # @random_reaction.error
    @emoji_random.error
    async def emoji_random_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, NotFound):
            return await error.handle(
                    ctx=ctx,
                    message=f"You don't seem to have any emojis enabled..."
            )

    @emoji.command(name="enable")
    @app_commands.describe(emoji="Choose an emoji")
    @permissions.is_bot_owner()
    async def emoji_enable(
            self,
            ctx: Interaction,
            emoji: Transform[discord.Emoji, AvailableEmojiTransformer]
    ):
        """Allow the given emoji to be used by the bot"""

        await self.emoji_service.enable_emoji(emoji.guild_id, emoji.id, emoji.name)
        await ctx.response.send_message(f"Enabled {str(emoji)}", ephemeral=True)

    @emoji.command(name="disable")
    @app_commands.describe(emoji="Choose an emoji")
    @permissions.is_bot_owner()
    async def emoji_disable(
            self,
            ctx: Interaction,
            emoji: Transform[discord.Emoji, EnabledEmojiTransformer]
    ):
        """Disallow the given emoji from being used by the bot"""

        await self.emoji_service.disable_emoji(emoji.id)
        await ctx.response.send_message(f"Disabled {str(emoji)}", ephemeral=True)
