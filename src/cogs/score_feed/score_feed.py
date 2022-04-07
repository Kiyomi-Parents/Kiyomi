from discord import slash_command
from discord.ext import commands

from src.cogs.scoresaber import ScoreSaberAPI
from src.cogs.settings.storage.model.channel_setting import ChannelSetting
from src.kiyomi import Kiyomi, permissions
from .score_feed_cog import ScoreFeedCog
from .services import SentScoreService, NotificationService
from src.cogs.scoresaber.storage.model.guild_player import GuildPlayer


class ScoreFeed(ScoreFeedCog, name="Score Feed"):
    def __init__(self, bot: Kiyomi, notification_service: NotificationService, sent_score_service: SentScoreService):
        super().__init__(bot, notification_service, sent_score_service)

        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("on_new_player")
        async def mark_scores_sent(guild_player: GuildPlayer):
            self.sent_score_service.mark_player_scores_sent(guild_player.player, guild_player.guild)

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ChannelSetting.create(self.bot, "Score feed channel", "score_feed_channel_id")
        ]

        self.bot.events.emit("setting_register", settings)

    @slash_command(**permissions.is_bot_owner_and_admin_guild())
    async def send_notifications(self, ctx):
        """Send recent score notifications."""
        await self.notification_service.send_notifications(ctx.guild.id)

        await ctx.respond("Doing the thing...")

    @slash_command(**permissions.is_bot_owner_and_admin_guild())
    async def mark_sent(self, ctx, player_id: str = None):
        """Mark all scores send for player."""
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        if player_id is None:
            players = scoresaber.get_players()

            for player in players:
                self.sent_score_service.mark_all_player_scores_sent(player)

            await ctx.respond(f"Marked scores as sent for {len(players)} players")
            return

        player = scoresaber.get_player(player_id)

        if player is None:
            await ctx.respond(f"Could not find player with id {player_id}")
            return

        self.sent_score_service.mark_all_player_scores_sent(player)
