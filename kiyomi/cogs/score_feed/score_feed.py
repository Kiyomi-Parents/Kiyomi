from discord import app_commands, Interaction
from discord.ext import commands

from kiyomi.cogs.scoresaber import ScoreSaberAPI
from kiyomi.cogs.settings.storage.model.channel_setting import ChannelSetting
from kiyomi.cogs.scoresaber.storage.model.guild_player import GuildPlayer
from kiyomi.cogs.scoresaber.storage.model.score import Score
from kiyomi import permissions, BaseCog
from .services import ServiceUnitOfWork


class ScoreFeed(BaseCog[ServiceUnitOfWork], name="Score Feed"):
    def register_events(self):
        @self.bot.events.on("on_new_player")
        async def mark_scores_sent(guild_player: GuildPlayer):
            await self.service_uow.sent_scores.mark_player_scores_sent(guild_player.guild_id, guild_player.player_id)
            await self.service_uow.save_changes()
            await self.service_uow.close()

        @self.bot.events.on("on_new_score_live")
        async def send_notifications_for_score(score: Score):
            for guild in score.player.guilds:
                await self.service_uow.notifications.send_notification(guild, score.player)
                await self.service_uow.save_changes()
                await self.service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [ChannelSetting.create(self.bot, "Score feed channel", "score_feed_channel_id")]

        self.bot.events.emit("setting_register", settings)

    score_feed = app_commands.Group(
        name="score_feed",
        description="Score feed related commands",
        guild_ids=permissions.admin_guild_list(),
    )

    @app_commands.command()
    @permissions.is_bot_owner()
    async def send_notifications(self, ctx: Interaction):
        """Send recent score notifications."""
        await self.service_uow.notifications.send_notifications(ctx.guild.id)
        await self.service_uow.save_changes()

        await ctx.response.send_message("Doing the thing...", ephemeral=True)

    @app_commands.command()
    @permissions.is_bot_owner()
    async def mark_sent(self, ctx: Interaction, player_id: str = None):
        """Mark all scores send for player."""
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        if player_id is None:
            players = await scoresaber.get_players()

            for player in players:
                await self.service_uow.sent_scores.mark_all_player_scores_sent(player)

            await self.service_uow.save_changes()

            await ctx.response.send_message(f"Marked scores as sent for {len(players)} players", ephemeral=True)
            return

        player = await scoresaber.get_player(player_id)

        if player is None:
            await ctx.response.send_message(f"Could not find player with id {player_id}", ephemeral=True)
            return

        await self.service_uow.sent_scores.mark_all_player_scores_sent(player)
        await self.service_uow.save_changes()
