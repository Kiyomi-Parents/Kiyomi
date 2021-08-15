import discord.member
from discord.ext import commands

from src.cogs.security import Security
from .actions import Actions
from .storage.uow import UnitOfWork
from src.cogs.scoresaber.storage.model.player import Player
from src.base.base_cog import BaseCog


class General(BaseCog):

    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):

        @self.uow.bot.events.on("on_new_player")
        def register_member(_player: Player, discord_member: discord.Member):
            self.actions.register_member(discord_member)
            self.actions.register_guild_member(discord_member)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.uow.bot.guilds:
            self.actions.register_guild(guild)

    @commands.command()
    async def hello(self, ctx):
        """Greet the bot."""
        await ctx.send("Hello there!")

    @commands.command(name="admintest")
    @Security.owner_or_permissions(administrator=True)
    async def admin_test(self, ctx):
        """Command to test if security is working"""
        await ctx.send("This message should only be seen if !admintest was called by a server admin.")
