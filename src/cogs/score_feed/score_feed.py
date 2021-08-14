import discord.member
from discord.ext import commands

from .actions import Actions
from .errors import GuildRecentChannelExistsException, GuildRecentChannelNotFoundException
from .storage.uow import UnitOfWork
from ..scoresaber.storage.model.player import Player
from ..security import Security


class ScoreFeed(commands.Cog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):

        @self.uow.bot.events.on("on_new_player")
        def mark_scores_sent(player: Player, _discord_member: discord.Member):
            self.actions.mark_all_player_scores_sent(player)

    @commands.group(invoke_without_command=True)
    @Security.owner_or_permissions(administrator=True)
    async def channel(self, ctx):
        """Set the recent score notification channel for ScoreSaber scores."""
        await ctx.send_help(ctx.command)

    @channel.command(name="add")
    async def channel_add(self, ctx):
        """Set current channel as the notification channel."""
        try:
            self.actions.add_score_feed_channel(ctx.guild.id, ctx.channel.id)
            await ctx.send(f"Channel **{ctx.channel.name}** has successfully set as the notification channel!")
        except GuildRecentChannelExistsException as error:
            await ctx.send(error)

    @channel.command(name="remove")
    async def channel_remove(self, ctx):
        """Remove the currently set notification channel."""
        try:
            self.actions.remove_score_feed_channel(ctx.guild.id)
            await ctx.send("Notifications channel successfully removed!")
        except GuildRecentChannelNotFoundException as error:
            await ctx.send(error)

    @commands.command()
    @Security.owner_or_permissions(administrator=True)
    async def send_notifications(self, ctx):
        """Send recent score notifications."""
        await self.actions.send_notifications(ctx.guild.id)
