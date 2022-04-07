from typing import List, Optional

from sqlalchemy.orm import Query

from src.kiyomi.database import BaseRepository
from src.log import Logger
from ..model.player import Player
from ..model.score import Score


class PlayerRepository(BaseRepository[Player]):

    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Player) \
            .filter(Player.id == entry_id)

    def get_all(self) -> Optional[List[Player]]:
        return self.session.query(Player) \
            .all()

    def add_score(self, player: Player, score: Score):
        player.scores.append(score)

        Logger.log(player, f"Added new {score}")
