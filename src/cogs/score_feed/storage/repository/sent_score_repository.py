from typing import Optional, List

from ..model import SentScore
from src.database import Repository


class SentScoreRepository(Repository):
    def get_by_id(self, entry_id: int) -> Optional[SentScore]:
        return self._db.session.query(SentScore)\
            .filter(SentScore.id == entry_id)\
            .first()

    def get_all(self) -> Optional[List[SentScore]]:
        return self._db.session.query(SentScore) \
            .all()

    def get_by_score_id_and_guild_id(self, score_id: int, guild_id: int) -> Optional[SentScore]:
        return self._db.session.query(SentScore) \
            .filter(SentScore.score_id == score_id) \
            .filter(SentScore.guild_id == guild_id) \
            .first()
