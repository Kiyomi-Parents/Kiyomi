from typing import List, Optional

import pyscoresaber

from src.log import Logger
from .scoresaber_service import ScoreSaberService
from ..storage.model.leaderboard import Leaderboard
from ..storage.model.player import Player
from ..storage.model.score import Score


class ScoreService(ScoreSaberService):

    def get_recent_scores(self, player_id: str, limit: int) -> List[Score]:
        return self.uow.scores.get_player_recent_scores(player_id, limit)

    # TODO: This can be optimized further, needs bulk leaderboard and score db inserting
    async def update_player_scores(self, player: Player):
        new_player_scores = await self.get_missing_recent_scores(player)
        Logger.log(player, f"Got {len(new_player_scores)} new recent scores from Score Saber")

        if len(new_player_scores) == 0:
            return

        new_leaderboards = []
        for new_player_score in new_player_scores:
            new_leaderboard = await self.add_new_leaderboard(new_player_score.leaderboard)

            if new_leaderboard is not None:
                new_leaderboards.append(new_leaderboard)

        new_scores = []
        for new_player_score in new_player_scores:
            new_scores.append(await self.add_new_score(player, new_player_score))

        self.uow.save_changes()

        for new_score in new_scores:
            self.uow.session.refresh(new_score)

        # Emit event for new leaderboards
        self.bot.events.emit("on_new_leaderboards", new_leaderboards)

        # Emit event for new scores
        self.bot.events.emit("on_new_scores", new_scores)

    async def add_new_leaderboard(self, leaderboard: pyscoresaber.LeaderboardInfo) -> Optional[Leaderboard]:
        if not self.uow.leaderboards.exists(leaderboard.id):
            return self.uow.leaderboards.add(Leaderboard(leaderboard))

        return None

    async def add_new_score(self, player: Player, player_score: pyscoresaber.PlayerScore) -> Score:
        new_score = Score(player_score)

        self.uow.players.add_score(player, new_score)

        return new_score

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
