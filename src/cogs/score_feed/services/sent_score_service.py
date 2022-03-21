from .score_feed_service import ScoreFeedService
from src.cogs.scoresaber import ScoreSaberAPI
from src.log import Logger
from src.cogs.scoresaber.storage import Player
from src.cogs.general.storage import Guild
from ..storage import SentScore


class SentScoreService(ScoreFeedService):

    def mark_all_guild_scores_sent(self, guild_id: int):
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)
        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        Logger.log(guild_players[0].guild, f"Marking scores sent for {len(guild_players)} players")

        for guild_player in guild_players:
            self.mark_player_scores_sent(guild_player.player, guild_player.guild)

    def mark_all_player_scores_sent(self, player: Player):
        Logger.log(player, "Marking all scores as sent")

        for guild in player.guilds:
            self.mark_player_scores_sent(player, guild)

    def mark_player_scores_sent(self, player: Player, guild: Guild):
        scores = self.uow.sent_score_repo.get_unsent_scores(guild.id, player.id)

        Logger.log(player, f"Marking {len(scores)} scores as sent in {guild}")

        sent_scores = []
        for score in scores:
            sent_scores.append(SentScore(score.id, guild.id))

        if len(sent_scores) != 0:
            self.uow.sent_score_repo.add_all(sent_scores)
