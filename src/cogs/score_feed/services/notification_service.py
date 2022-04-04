from src.cogs.scoresaber import ScoreSaberAPI
from src.cogs.settings import SettingsAPI
from src.log import Logger
from .score_feed_service import ScoreFeedService
from ..messages.views.ScoreNotificationView import ScoreNotificationView
from ..storage.model.sent_score import SentScore
from src.cogs.general.storage.model.guild import Guild
from ...scoresaber.storage.model.player import Player


class NotificationService(ScoreFeedService):

    async def send_notifications(self, guild_id: int):
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)
        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        Logger.log(guild_players[0].guild, f"Sending notifications for {len(guild_players)} players")

        for guild_player in guild_players:
            await self.send_notification(guild_player.guild, guild_player.player)

    async def send_notification(self, guild: Guild, player: Player) -> None:
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)
        settings = self.bot.get_cog_api(SettingsAPI)

        channel = settings.get(guild.id, "score_feed_channel_id")

        if channel is None:
            Logger.log(guild, "Recent scores channel not found, skipping!")
            return

        discord_guild = self.bot.get_guild(guild.id)
        scores = self.uow.sent_score_repo.get_unsent_scores(guild.id, player.id)

        Logger.log(guild, f"{player} has {len(scores)} scores to notify")

        for score in scores:
            previous_score = scoresaber.get_previous_score(score)

            song_view = ScoreNotificationView(self.bot, discord_guild, score, previous_score)
            await song_view.send(target=channel)

            self.uow.sent_score_repo.add(SentScore(score.id, guild.id))
