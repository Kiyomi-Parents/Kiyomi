from typing import List

from src.cogs.beatsaber.leaderboard.leaderboard_score import LeaderboardScore
from src.storage.model import DiscordGuild
from src.storage.uow import UnitOfWork


class Leaderboard:
    def __init__(self, uow: UnitOfWork, db_guild: DiscordGuild, leaderboard_id: int):
        self._uow = uow
        self._db_guild = db_guild
        self._leaderboard_id = leaderboard_id

    @staticmethod
    def sort_leaderboard(leaderboard_scores: List[LeaderboardScore]) -> List[LeaderboardScore]:
        return sorted(leaderboard_scores, key=lambda leaderboard_score: leaderboard_score.db_score.score, reverse=True)
