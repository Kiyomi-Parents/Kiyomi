from typing import List

from src.cogs.beatsaber.leaderboard.leaderboard import Leaderboard
from src.cogs.beatsaber.leaderboard.leaderboard_score import LeaderboardScore


class GuildLeaderboard(Leaderboard):

    @property
    def leaderboard_scores(self) -> List[LeaderboardScore]:
        leaderboard = []

        for db_player in self._db_guild.players:
            db_score = self._uow.score_repo.get_player_best_score_on_leaderboard(db_player, self._leaderboard_id)

            if db_score is not None:
                leaderboard.append(LeaderboardScore(db_player, db_score))

        return self.sort_leaderboard(leaderboard)
