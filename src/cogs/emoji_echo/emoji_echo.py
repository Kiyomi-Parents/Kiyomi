import discord
from discord import SlashCommandGroup, Option, ApplicationCommandInvokeError, ApplicationContext, slash_command, \
    Permissions, message_command
from discord.ext import commands
from discord.ext.commands import EmojiConverter

from src.cogs.emoji_echo.emoji_echo_cog import EmojiEchoCog
from src.cogs.emoji_echo.errors import EmojiEchoCogException, NotFound
from src.cogs.settings import SettingsAPI
from src.cogs.settings.storage import ToggleSetting
from src.kiyomi import permissions


class EmojiEcho(EmojiEchoCog):

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
            emoji = self.emoji_service.get_emoji_from_message(msg.guild.id, msg.content)

            if emoji is not None:
                await msg.channel.send(emoji)

    emoji = SlashCommandGroup(
            "emoji",
            "Emojis that Kiyomi is allowed to play with",
            **permissions.is_bot_owner()
    )

    @message_command(name="Random reaction")
    async def random_reaction(self, ctx: discord.ApplicationContext, message: discord.Message):
        emoji = await self.emoji_service.get_random_enabled_emoji()

        await message.add_reaction(emoji)
        await ctx.delete()

    @slash_command(name="emoji-random")
    async def emoji_random(self, ctx: discord.ApplicationContext):
        """Posts a random enabled emoji"""
        emoji = await self.emoji_service.get_random_enabled_emoji()

        await ctx.delete()
        await ctx.send(str(emoji))

    @random_reaction.error
    @emoji_random.error
    async def emoji_random_error(self, ctx: discord.ApplicationContext, error: Exception):
        if isinstance(error, ApplicationCommandInvokeError):
            if isinstance(error.original, NotFound):
                return await error.original.handle(ctx, f"You don't seem to have any emojis enabled...")

    # @emoji.command(name="all", default_permission=False)
    # @permissions.is_bot_owner()
    # @permissions.is_guild_only()
    # async def emoji_all(self, ctx: discord.ApplicationContext):
    #     """Posts all the emojis, not a good idea to use :)"""
    #     emoji_list = []
    #
    #     for emoji in self.bot.emojis:
    #         emoji_list.append(str(self.bot.get_emoji(emoji.id)))
    #
    #         if len(emoji_list) >= 20:
    #             await ctx.respond("".join(emoji_list))
    #             emoji_list.clear()
    #
    #     await ctx.respond("".join(emoji_list))

    # Workaround
    async def get_available_emojis(self, ctx: discord.AutocompleteContext):
        return await self.emoji_autocomplete_service.get_available_emojis(ctx)

    @emoji.command(name="enable", **permissions.is_bot_owner())
    async def emoji_enable(
        self,
        ctx: discord.ApplicationContext,
        emoji: Option(
                EmojiConverter,
                "Choose an emoji",
                autocomplete=get_available_emojis
        )
    ):
        """Allow the given emoji to be used by the bot"""

        await self.emoji_service.enable_emoji(emoji.guild_id, emoji.id, emoji.name)
        await ctx.respond(f"Enabled {str(emoji)}", ephemeral=True)

    # Workaround
    async def get_enabled_emojis(self, ctx: discord.AutocompleteContext):
        return await self.emoji_autocomplete_service.get_enabled_emojis(ctx)

    @emoji.command(name="disable", **permissions.is_bot_owner())
    async def emoji_disable(self,
        ctx: discord.ApplicationContext,
        emoji: Option(
                EmojiConverter,
                "Choose an emoji",
                autocomplete=get_enabled_emojis
        )
    ):
        """Disallow the given emoji from being used by the bot"""

        await self.emoji_service.disable_emoji(emoji.id)
        await ctx.respond(f"Disabled {str(emoji)}", ephemeral=True)

    async def cog_command_error(self, ctx: ApplicationContext, error: Exception):
        if isinstance(error, ApplicationCommandInvokeError):
            if isinstance(error.original, EmojiEchoCogException):
                return await error.original.handle(ctx)
