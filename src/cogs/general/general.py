import random

import discord.member
from discord.ext import commands

from src.cogs.security import Security
from .actions import Actions
from .storage.uow import UnitOfWork
from src.cogs.scoresaber.storage.model.player import Player
from src.base.base_cog import BaseCog
from ...utils import Utils


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

    @commands.command(name="emoji", hidden=True)
    async def random_emoji(self, ctx: Context):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send(self.uow.bot.get_emoji(self.uow.bot.emojis[random.randint(0, len(self.uow.bot.emojis)-1)].id))

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
