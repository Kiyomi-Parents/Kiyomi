from typing import List, Optional

import pybeatsaver

from kiyomi.cogs.beatsaver import BeatSaverAPI
from kiyomi.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from kiyomi.cogs.scoresaber import ScoreSaberAPI
from kiyomi.cogs.scoresaber.storage.model.player import Player
from kiyomi.cogs.scoresaber.storage.model.score import Score
from ..storage import StorageUnitOfWork
from kiyomi.service.base_basic_service import BaseBasicService


class ScoreLeaderboardService(BaseBasicService[StorageUnitOfWork]):
    async def get_beatmap_score_leaderboard_by_key(
        self,
        guild_id: int,
        beatmap_key: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> List[Score]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        beatmap_hash = await beatsaver.get_beatmap_hash_by_key(beatmap_key)

        if beatmap_hash is None:
            return []

        return await self.get_beatmap_score_leaderboard(guild_id, beatmap_hash, characteristic, difficulty)

    async def get_beatmap_score_leaderboard(
        self,
        guild_id: int,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> List[Score]:
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        leaderboard = await scoresaber.get_leaderboard(
            beatmap_hash,
            BeatSaverUtils.to_scoresaber_game_mode(characteristic),
            BeatSaverUtils.to_scoresaber_difficulty(difficulty),
        )

        if leaderboard is None:
            return []

        guild_players = await scoresaber.get_guild_players_by_guild(guild_id)

        return await self._get_score_leaderboard([guild_player.player for guild_player in guild_players], leaderboard.id)

    async def _get_score_leaderboard(self, players: List[Player], leaderboard_id: int) -> List[Score]:
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        score_leaderboard = []

        for player in players:
            scores = await scoresaber.get_score_by_player_id_and_leaderboard_id(player.id, leaderboard_id)
            best_score = self.get_best_score(scores)

            if best_score is not None:
                score_leaderboard.append(best_score)

        score_leaderboard.sort(key=lambda score: score.modified_score, reverse=True)

        return score_leaderboard

    @staticmethod
    def get_best_score(scores: List[Score]) -> Optional[Score]:
        best_score = None

        for score in scores:
            if best_score is None:
                best_score = score
                continue

            # Not sure if modified_score is the best thing to use here
            if score.modified_score > best_score.modified_score:
                best_score = score

        return best_score

    async def get_player_top_scores_leaderboard(self, player_id: str) -> List[Score]:
        from kiyomi.cogs.scoresaber import ScoreSaberAPI

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        scores = await scoresaber.get_player_scores_sorted_by_pp(player_id)
        unique_scores = []

        for score in scores:
            if score.score_id not in [unique_score.score_id for unique_score in unique_scores]:
                unique_scores.append(score)

        return unique_scores
