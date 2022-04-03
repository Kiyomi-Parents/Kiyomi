from typing import List, Optional

import pybeatsaver

from src.cogs.beatsaver import BeatSaverAPI
from src.cogs.beatsaver.storage.model.beatmap import Beatmap
from src.cogs.beatsaver.storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.cogs.leaderboard.services.leaderboard_service import LeaderboardService
from src.cogs.scoresaber import ScoreSaberAPI
from src.cogs.scoresaber.storage.model.player import Player
from src.cogs.scoresaber.storage.model.score import Score


class ScoreLeaderboardService(LeaderboardService):

    async def get_beatmap_score_leaderboard_by_key(self, guild_id: int, beatmap_key: str, characteristic: pybeatsaver.ECharacteristic, difficulty: pybeatsaver.EDifficulty) -> List[Score]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        beatmap_difficulty = await beatsaver.get_beatmap_difficulty_by_beatmap_key(beatmap_key, characteristic, difficulty)

        if beatmap_difficulty is None:
            return []

        return await self.get_beatmap_score_leaderboard(guild_id, beatmap_difficulty)

    async def get_beatmap_score_leaderboard_by_beatmap(self, guild_id: int, beatmap: Beatmap, characteristic: pybeatsaver.ECharacteristic, difficulty: pybeatsaver.EDifficulty) -> List[Score]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        beatmap_difficulty = beatsaver.get_beatmap_difficulty_by_beatmap(
                beatmap,
                characteristic,
                difficulty
        )

        if beatmap_difficulty is None:
            return []

        return await self.get_beatmap_score_leaderboard(guild_id, beatmap_difficulty)

    async def get_beatmap_score_leaderboard(self, guild_id: int, beatmap_difficulty: BeatmapVersionDifficulty) -> List[Score]:
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        leaderboard = scoresaber.uow.leaderboards.get_by_song_hash(
                beatmap_difficulty.beatmap_version.hash,
                beatmap_difficulty.characteristic,
                beatmap_difficulty.difficulty
        )

        if leaderboard is None:
            return []

        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        return self._get_score_leaderboard([guild_player.player for guild_player in guild_players], leaderboard.id)

    def _get_score_leaderboard(self, players: List[Player], leaderboard_id: int) -> List[Score]:
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        score_leaderboard = []

        for player in players:
            scores = scoresaber.get_score_by_player_id_and_leaderboard_id(player.id, leaderboard_id)
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

    def get_player_top_scores_leaderboard(self, player_id: str) -> List[Score]:
        from src.cogs.scoresaber import ScoreSaberAPI

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        scores = scoresaber.get_player_scores_sorted_by_pp(player_id)
        unique_scores = []

        for score in scores:
            if score.score_id not in [unique_score.score_id for unique_score in unique_scores]:
                unique_scores.append(score)

        return unique_scores
