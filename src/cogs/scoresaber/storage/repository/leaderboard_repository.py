from typing import Optional, List

import pyscoresaber
from sqlalchemy.orm import Query

from ..model.leaderboard import Leaderboard
from src.kiyomi.database import BaseRepository


class LeaderboardRepository(BaseRepository[Leaderboard]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Leaderboard) \
            .filter(Leaderboard.id == entry_id)

    def get_all(self) -> Optional[List[Leaderboard]]:
        return self.session.query(Leaderboard) \
            .all()

    def get_by_song_hash(self,
        song_hash: str,
        song_game_mode: pyscoresaber.GameMode,
        song_difficulty: pyscoresaber.BeatmapDifficulty
    ) -> Optional[Leaderboard]:
        return self.session.query(Leaderboard) \
            .filter(Leaderboard.song_hash == song_hash) \
            .filter(Leaderboard.game_mode == song_game_mode.name) \
            .filter(Leaderboard.difficulty == song_difficulty.name) \
            .first()
