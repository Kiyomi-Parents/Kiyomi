from discord import slash_command
from discord.ext import commands

from src.cogs.scoresaber.storage.model.guild_player import GuildPlayer
from src.cogs.security import Security
from src.cogs.settings.storage.model.ChannelSetting import ChannelSetting
from src.kiyomi.base_cog import BaseCog
from .actions import Actions
from .storage.uow import UnitOfWork


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

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ChannelSetting.create(self.uow.bot, "score_feed_channel_id", None)
        ]

        self.uow.bot.events.emit("setting_register", settings)

    @slash_command()
    @Security.owner_or_permissions(administrator=True)
    async def send_notifications(self, ctx):
        """Send recent score notifications."""
        await self.actions.send_notifications(ctx.guild.id)

    @slash_command()
    @Security.owner_or_permissions(administrator=True)
    async def mark_sent(self, ctx, player_id: str = None):
        """Mark all scores send for player."""
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")

        if player_id is None:
            players = scoresaber.get_players()

            for player in players:
                self.actions.mark_all_player_scores_sent(player)

            await ctx.respond(f"Marked scores as sent for {len(players)} players")
            return

        player = scoresaber.get_player(player_id)

        if player is None:
            await ctx.respond(f"Could not find player with id {player_id}")
            return

        self.actions.mark_all_player_scores_sent(player)
