from src.log import Logger
from .score_feed_service import ScoreFeedService
from src.cogs.scoresaber import ScoreSaberAPI
from src.cogs.general.storage import Guild
from src.cogs.scoresaber.storage import Player
from src.cogs.settings import SettingsAPI
from ..message import Message
from ..storage import SentScore


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

        scores = self.uow.sent_score_repo.get_unsent_scores(guild.id, player.id)

        Logger.log(guild, f"{player} has {len(scores)} scores to notify")

        for score in scores:
            previous_score = scoresaber.get_previous_score(score)

            if previous_score is None:
                # Post as new score
                embed = Message.get_new_score_embed(player, score, score.leaderboard.beatmap_version)
            else:
                # Post as improvement
                previous_score = scoresaber.update_score_pp_weight(previous_score)
                embed = Message.get_improvement_score_embed(player, previous_score, score, score.leaderboard.beatmap_version)

            await channel.send(embed=embed)
            self.uow.sent_score_repo.add(SentScore(score.id, guild.id))

            # TODO: FIX LATER
            # Guild snipes leaderboard
            # if db_guild.guild_snipes:
            #     leaderboard = GuildLeaderboard(self.uow, db_guild, db_score.leaderboard_id)
            #
            #     if len(leaderboard.leaderboard_scores) > 0:
            #         guild_leaderboard_embed = Message.get_leaderboard_embed(leaderboard.get_top_scores(3))
            #         await channel.send(embed=guild_leaderboard_embed)