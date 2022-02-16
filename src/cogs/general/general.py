import discord.member
from discord import SlashCommandGroup, Option
from discord.ext import commands
from discord.ext.commands import EmojiNotFound

from src.cogs.security import Security
from src.kiyomi.base_cog import BaseCog
from src.utils import Utils
from .actions import Actions
from .errors import EmojiAlreadyExistsException, EmojiNotFoundException
from .storage.uow import UnitOfWork


class General(BaseCog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):
        @self.uow.bot.events.on("register_member")
        async def register_member(discord_member: discord.Member):
            self.actions.register_member(discord_member)
            self.actions.register_guild_member(discord_member)

    @commands.Cog.listener()
    async def on_ready(self):
        for discord_guild in self.uow.bot.guilds:
            self.actions.register_guild(discord_guild)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Repost emoji if enabled"""
        if msg.author.id == self.uow.bot.user.id:
            return

        settings = self.uow.bot.get_cog("SettingsAPI")

        if settings.get(msg.guild.id, "repost_emoji"):
            emoji = self.actions.get_emoji_from_message(msg.content)
            if emoji is not None:
                await msg.channel.send(emoji)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.actions.register_guild(guild)

    @commands.slash_command()
    async def hello(self, ctx):
        """Greet the bot"""
        await ctx.respond("Hello there!")

    @commands.slash_command()
    @Security.is_owner()
    async def say(self, ctx, text: str):
        """I repeat what you say"""
        await ctx.respond(text)

    status = SlashCommandGroup(
        "status", "Commands related to Kiyomi's status"
    )

    @status.command(name="update")
    @Security.is_owner()
    @Utils.update_tasks_list
    async def status_update(self, ctx):
        """owo"""
        await ctx.respond("status should've updated")

    emoji = SlashCommandGroup(
        "emoji",
        "Emojis that Kiyomi is allowed to play with",
        guild_ids=[198040147189694464]
    )

    @emoji.command(name="random")
    async def emoji_random(self, ctx):
        """Posts a random enabled emoji"""
        emoji = await self.actions.get_random_enabled_emoji()
        await ctx.respond(str(emoji))

    @emoji.command(name="all")
    @Security.is_owner()
    async def emoji_all(self, ctx):
        """Posts all the emojis, not a good idea to use :)"""
        emoji_list = []

        for emoji in self.uow.bot.emojis:
            emoji_list.append(str(self.uow.bot.get_emoji(emoji.id)))

            if len(emoji_list) >= 20:
                await ctx.respond("".join(emoji_list))
                emoji_list.clear()

        await ctx.respond("".join(emoji_list))

    # Workaround
    async def get_available_emojis(self, ctx: discord.AutocompleteContext):
        return await self.actions.get_available_emojis(ctx)

    @emoji.command(name="enable", guild_ids=[198040147189694464])
    @Security.is_owner()
    async def emoji_enable(
        self,
        ctx: discord.ApplicationContext,
        emoji: Option(
            str,
            "Choose an emoji",
            autocomplete=get_available_emojis
        )
    ):
        """Allow the given emoji to be used by the bot"""
        try:
            obj_emoji = self.uow.bot.get_emoji(int(emoji))

            await self.actions.enable_emoji(obj_emoji.id, obj_emoji.guild_id, obj_emoji.name)
            await ctx.respond(f"Enabled {str(obj_emoji)}")
        except EmojiAlreadyExistsException as error:
            await ctx.respond(str(error))

    # Workaround
    async def get_enabled_emojis(self, ctx: discord.AutocompleteContext):
        return await self.actions.get_enabled_emojis(ctx)

    @emoji.command(name="disable", guild_ids=[198040147189694464])
    @Security.is_owner()
    async def emoji_disable(self,
        ctx: discord.ApplicationContext,
        emoji: Option(
            str,
            "Choose an emoji",
            autocomplete=get_enabled_emojis
        )
    ):
        """Disallow the given emoji from being used by the bot"""
        try:
            obj_emoji = self.uow.bot.get_emoji(int(emoji))

            await self.actions.disable_emoji(obj_emoji.id)
            await ctx.respond(f"Disabled {str(obj_emoji)}")
        except EmojiNotFoundException as error:
            await ctx.respond(str(error))

    @emoji_enable.error
    @emoji_disable.error
    async def emoji_error(self, ctx, error):
        if isinstance(error, EmojiNotFound):
            await ctx.respond("You can't use unicode emojis and emojis from servers the bot isn't in!")
        return
