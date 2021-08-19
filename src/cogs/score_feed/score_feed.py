from discord.ext import commands
from discord.ext.commands import Context

from src.kiyomi.base_cog import BaseCog
from src.cogs.security import Security
from .actions import Actions
from .errors import GuildRecentChannelExistsException, GuildRecentChannelNotFoundException
from .storage.uow import UnitOfWork
from ..scoresaber.storage.model.guild_player import GuildPlayer


class ScoreFeed(BaseCog, name="Score Feed"):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):

        @self.uow.bot.events.on("on_new_player")
        async def mark_scores_sent(guild_player: GuildPlayer):
            self.actions.mark_player_scores_sent(guild_player.player, guild_player.guild)

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

    @commands.command()
    @Security.owner_or_permissions(administrator=True)
    async def mark_sent(self, ctx: Context, player_id: str = None):
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")

        if player_id is None:
            players = scoresaber.get_players()

            for player in players:
                self.actions.mark_all_player_scores_sent(player)

            return

        player = scoresaber.get_player(player_id)

        if player is None:
            await ctx.send(f"Could not find player with id {player_id}")
            return

        self.actions.mark_all_player_scores_sent(player)
