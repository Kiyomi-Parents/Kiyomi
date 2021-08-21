import discord.member
from discord.ext import commands
from discord.ext.commands import Context

from src.cogs.security import Security
from .actions import Actions
from .errors import EmojiAlreadyExistsException, EmojiNotFoundException
from .storage.uow import UnitOfWork
from src.kiyomi.base_cog import BaseCog
from src.utils import Utils


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
    async def on_guild_join(self, guild: discord.Guild):
        self.actions.register_guild(guild)

    @commands.command()
    async def hello(self, ctx):
        """Greet the bot."""
        await ctx.send("Hello there!")

    @commands.command(name="many emoji", hidden=True)
    @Security.is_owner()
    async def many_emoji(self, ctx):
        emoji_list = []
        for emoji in self.uow.bot.emojis:
            emoji_list.append(str(self.uow.bot.get_emoji(emoji.id)))
            if len(emoji_list) >= 20:
                await ctx.send("".join(emoji_list))
                emoji_list.clear()
        await ctx.send("".join(emoji_list))

    @commands.command(name="su", hidden=True)
    @Security.is_owner()
    @Utils.update_tasks_list
    async def status_update(self, ctx):
        """owo"""
        await ctx.send("status should've updated")

    @commands.command(name="admintest", hidden=True)
    @Security.owner_or_permissions(administrator=True)
    async def admin_test(self, ctx):
        """Command to test if security is working"""
        await ctx.send("This message should only be seen if !admintest was called by a server admin.")

    @commands.group(invoke_without_command=True)
    async def emoji(self, ctx: Context):
        if ctx.subcommand_passed is None:
            emoji = await self.actions.get_random_enabled_emoji()
            await ctx.send(str(emoji))

    @emoji.command(name="enable", hidden=True)
    @Security.is_owner()
    async def emoji_enable(self, ctx: Context, emoji: discord.Emoji):
        """Allow the given emoji to be used by the bot"""
        try:
            await self.actions.enable_emoji(emoji.id, emoji.guild_id, emoji.name)
            await ctx.send(f"Enabled {str(emoji)}")
        except EmojiAlreadyExistsException as error:
            await ctx.send(str(error))

    @emoji.command(name="disable", hidden=True)
    @Security.is_owner()
    async def emoji_disable(self, ctx: Context, emoji: discord.Emoji):
        """Disallow the given emoji from being used by the bot"""
        try:
            await self.actions.disable_emoji(emoji.id)
            await ctx.send(f"Disabled {str(emoji)}")
        except EmojiNotFoundException as error:
            await ctx.send(str(error))
