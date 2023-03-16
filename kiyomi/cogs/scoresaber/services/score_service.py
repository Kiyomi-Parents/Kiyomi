import logging
from typing import List, Optional

import pyscoresaber

from kiyomi import BaseService, Kiyomi
from ..scoresaber_utils import ScoreSaberUtils
from ..storage import StorageUnitOfWork
from ..storage.model.leaderboard import Leaderboard
from ..storage.model.player import Player
from ..storage.model.score import Score
from ..storage.repository.score_repository import ScoreRepository

_logger = logging.getLogger(__name__)


class ScoreService(BaseService[Score, ScoreRepository, StorageUnitOfWork]):
    def __init__(
        self,
        bot: Kiyomi,
        repository: ScoreRepository,
        storage_uow: StorageUnitOfWork,
        scoresaber: pyscoresaber.ScoreSaberAPI,
    ):
        super().__init__(bot, repository, storage_uow)

        self.scoresaber = scoresaber

    async def get_recent_scores(self, player_id: str, limit: int) -> List[Score]:
        return await self.repository.get_recent(player_id, limit)

    async def get_previous_score(self, score: Score) -> Optional[Score]:
        previous_score = await self.repository.get_previous(score)

        if previous_score is None:
            return None

        return await self.update_score_pp_weight(previous_score)

    async def on_new_live_score_feed_score(self, player_score: pyscoresaber.PlayerScore):
        if not await self.is_player_score_new(player_score):
            return

        _logger.info(
            f"{player_score.score.leaderboard_player_info.name}",
            f"Got new score from Score Saber websocket",
        )

        if not await self.storage_uow.leaderboards.exists(player_score.leaderboard.id):
            new_leaderboard = await self.storage_uow.leaderboards.add(Leaderboard(player_score.leaderboard))
            self.bot.events.emit("on_new_leaderboards", [new_leaderboard])

        new_score = await self.repository.add(Score(player_score))
        self.bot.events.emit("on_new_scores", [new_score])

        self.bot.events.emit("on_new_score_live", new_score)

    async def update_player_scores(self, player: Player):
        new_player_scores = await self.get_missing_recent_scores(player)
        _logger.info(player, f"Got {len(new_player_scores)} new recent scores from Score Saber")

        if len(new_player_scores) == 0:
            return

        new_leaderboards = await self.get_new_leaderboards(
            [new_player_score.leaderboard for new_player_score in new_player_scores]
        )
        if len(new_leaderboards) > 0:
            await self.storage_uow.leaderboards.add_all(new_leaderboards)

        new_scores = self.get_new_scores(player, new_player_scores)
        if len(new_scores) > 0:
            await self.repository.add_all(new_scores)

        # Emit event for new leaderboards
        self.bot.events.emit("on_new_leaderboards", new_leaderboards)

        # Emit event for new scores
        self.bot.events.emit("on_new_scores", new_scores)

    async def get_new_leaderboards(self, leaderboards: List[pyscoresaber.LeaderboardInfo]) -> List[Leaderboard]:
        new_leaderboards = []

        for leaderboard in leaderboards:
            if not await self.storage_uow.leaderboards.exists(leaderboard.id):
                new_leaderboards.append(Leaderboard(leaderboard))

        return new_leaderboards

    def get_new_scores(self, player: Player, player_scores: List[pyscoresaber.PlayerScore]) -> List[Score]:
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
                    if await self.is_player_score_new(player_score):
                        return new_player_scores
                    else:
                        new_player_scores.append(player_score)

                _logger.info(
                    player,
                    f"Found {len(new_player_scores) - before_page_add_count} new scores from Score Saber",
                )
        except pyscoresaber.NotFoundException as error:
            _logger.info(
                player,
                f"Got HTTP code {error.status} when trying to access {error.url}",
            )

        return new_player_scores

    async def is_player_score_new(self, player_score: pyscoresaber.PlayerScore) -> bool:
        return await self.repository.exists_by_score_id_and_time_set(player_score.score.id, player_score.score.time_set)

    async def get_all_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> List[Score]:
        return await self.repository.get_all_by_player_id_and_leaderboard_id(player_id, leaderboard_id)

    async def get_best_score_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> Optional[Score]:
        return await self.repository.get_best_score_by_player_id_and_leaderboard_id(player_id, leaderboard_id)

    async def get_player_top_scores(self, player_id: str) -> List[Score]:
        scores = await self.repository.get_all_sorted_by_pp(player_id)
        unique_scores = []

        for score in scores:
            if score.score_id not in [unique_score.score_id for unique_score in unique_scores]:
                unique_scores.append(score)

        return unique_scores

    async def update_score_pp_weight(self, score: Score) -> Score:
        top_scores = await self.get_player_top_scores(score.player_id)

        position = 0

        for top_score in top_scores:
            if top_score.score_id == score.score_id:
                continue

            position += 1

            if top_score.pp < score.pp and position:
                break

        score.weight = ScoreSaberUtils.get_pp_weight_from_pos(position)

        return score
