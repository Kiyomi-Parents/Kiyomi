from typing import List, Optional

from kiyomi.cogs.scoresaber.storage.model.leaderboard import Leaderboard
from kiyomi.cogs.scoresaber.storage.model.score import Score


class GuildLeaderboard:
    def __init__(self, leaderboard: Optional[Leaderboard] = None, scores: Optional[List[Score]] = None):
        if scores is None:
            scores = []

        self.leaderboard: Optional[Leaderboard] = leaderboard
        self._scores: List[Score] = scores

    def add_score(self, score: Score):
        self._scores.append(score)

    @property
    def scores(self) -> List[Score]:
        self._scores.sort(key=lambda score: score.modified_score, reverse=True)

        return self._scores
