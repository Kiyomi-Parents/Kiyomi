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
            await self._service_uow.sent_scores.mark_player_scores_sent(guild_player.guild_id, guild_player.player_id)
            await self._service_uow.save_changes()
            await self._service_uow.close()

        @self.bot.events.on("on_new_score_live")
        async def send_notifications_for_score(score: Score):
            for guild in score.player.guilds:
                await self._service_uow.notifications.send_notification(guild, score.player)
                await self._service_uow.save_changes()
                await self._service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [ChannelSetting.create(self.bot, self.__cog_name__, "Score feed channel", "score_feed_channel_id")]

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
        await ctx.response.defer(ephemeral=True)

        await self._service_uow.notifications.send_notifications(ctx.guild.id)
        await self._service_uow.save_changes()

        await ctx.followup.send("Doing the thing...", ephemeral=True)

    @app_commands.command()
    @permissions.is_bot_owner()
    async def mark_sent(self, ctx: Interaction, player_id: str = None):
        """Mark all scores send for player."""
        await ctx.response.defer(ephemeral=True)

        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber:
            if player_id is None:
                players = await scoresaber.get_players()

                for player in players:
                    await self._service_uow.sent_scores.mark_all_player_scores_sent(player)

                await self._service_uow.save_changes()

                await ctx.followup.send(f"Marked scores as sent for {len(players)} players", ephemeral=True)
                return

            player = await scoresaber.get_player(player_id)

        if player is None:
            await ctx.followup.send(f"Could not find player with id {player_id}", ephemeral=True)
            return

        await self._service_uow.sent_scores.mark_all_player_scores_sent(player)
        await self._service_uow.save_changes()
