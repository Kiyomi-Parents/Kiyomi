from typing import List

import pyscoresaber

from src.log import Logger
from .scoresaber_service import ScoreSaberService
from ..storage.model.leaderboard import Leaderboard
from ..storage.model.player import Player
from ..storage.model.score import Score


class ScoreService(ScoreSaberService):

    def get_recent_scores(self, player_id: str, limit: int) -> List[Score]:
        return self.uow.scores.get_player_recent_scores(player_id, limit)

    async def update_player_scores(self, player: Player):
        new_player_scores = await self.get_missing_recent_scores(player)
        Logger.log(player, f"Got {len(new_player_scores)} new recent scores from Score Saber")

        if len(new_player_scores) == 0:
            return

        new_leaderboards = await self.get_new_leaderboards([new_player_score.leaderboard for new_player_score in new_player_scores])
        if len(new_leaderboards) > 0:
            self.uow.leaderboards.add_all(new_leaderboards)

        new_scores = await self.get_new_scores(player, new_player_scores)
        if len(new_scores) > 0:
            self.uow.scores.add_all(new_scores)

        self.uow.save_changes()

        # Emit event for new leaderboards
        self.bot.events.emit("on_new_leaderboards", new_leaderboards)

        # Emit event for new scores
        self.bot.events.emit("on_new_scores", new_scores)

    async def get_new_leaderboards(self, leaderboards: List[pyscoresaber.LeaderboardInfo]) -> List[Leaderboard]:
        new_leaderboards = []

        for leaderboard in leaderboards:
            if not self.uow.leaderboards.exists(leaderboard.id):
                new_leaderboards.append(Leaderboard(leaderboard))

        return new_leaderboards

    async def get_new_scores(self, player: Player, player_scores: List[pyscoresaber.PlayerScore]) -> List[Score]:
        new_scores = []

        for player_score in player_scores:
            new_score = Score(player_score)
            new_score.player_id = player.id

            new_scores.append(new_score)

        return new_scores

    async def get_missing_recent_scores(self, player: Player) -> List[pyscoresaber.PlayerScore]:
        new_player_scores = []

        try:
            async for player_scores in self.scoresaber.player_scores_all(int(player.id), pyscoresaber.ScoreSort.RECENT):
                before_page_add_count = len(new_player_scores)

                for player_score in player_scores:
                    if self.uow.scores.exists_by_score_id_and_time_set(player_score.score.id, player_score.score.time_set):
                        return new_player_scores
                    else:
                        new_player_scores.append(player_score)

                Logger.log(player, f"Found {len(new_player_scores) - before_page_add_count} new scores from Score Saber")
        except pyscoresaber.NotFoundException as error:
            Logger.log(player, f"Got HTTP code {error.status} when trying to access {error.url}")

        return new_player_scores
