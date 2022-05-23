from src.cogs.scoresaber import ScoreSaberAPI, ScoreSaberUI
from src.cogs.settings import SettingsAPI
from src.kiyomi import Kiyomi
from src.log import Logger
from .score_feed_service import ScoreFeedService
from .sent_score_service import SentScoreService
from ..storage.unit_of_work import UnitOfWork
from ..storage.model.sent_score import SentScore
from src.cogs.general.storage.model.guild import Guild
from ...scoresaber.storage.model.player import Player


class NotificationService(ScoreFeedService):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork, sent_score_service: SentScoreService):
        super().__init__(bot, uow)

        self.sent_score_service = sent_score_service

    async def send_notifications(self, guild_id: int):
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)
        guild_players = await scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        Logger.log(guild_players[0].guild, f"Sending notifications for {len(guild_players)} players")

        for guild_player in guild_players:
            await self.send_notification(guild_player.guild, guild_player.player)

    async def send_notification(self, guild: Guild, player: Player) -> None:
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)
        settings = self.bot.get_cog_api(SettingsAPI)

        channel_id = await settings.get(guild.id, "score_feed_channel_id")

        if channel_id is None:
            Logger.log(guild, "Recent scores channel not found, skipping!")
            return

        if not self.sent_score_service.should_send_scores(guild, player):
            Logger.log(guild, "Decided not to send scores. (Spam prevention)")
            await self.sent_score_service.mark_player_scores_sent(player, guild)
            return

        discord_guild = self.bot.get_guild(guild.id)
        scores = await self.uow.sent_score_repo.get_unsent_scores(guild.id, player.id)

        Logger.log(guild, f"{player} has {len(scores)} scores to notify")

        for score in scores:
            previous_score = await scoresaber.get_previous_score(score)

            scoresaber_ui = self.bot.get_cog_api(ScoreSaberUI)
            score_view = scoresaber_ui.view_score(self.bot, discord_guild, score, previous_score)
            await score_view.send(target=channel_id)

            async with self.uow:
                await self.uow.sent_score_repo.add(SentScore(score.id, guild.id))
