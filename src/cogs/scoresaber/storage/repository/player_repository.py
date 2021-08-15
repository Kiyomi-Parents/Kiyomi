from typing import List, Optional

from src.database import Repository
from src.log import Logger
from ..model.player import Player
from ..model.score import Score


class PlayerRepository(Repository[Player]):

    def get_by_id(self, entry_id: int) -> Optional[Player]:
        return self._db.session.query(Player) \
            .filter(Player.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Player]]:
        return self._db.session.query(Player) \
            .all()

    def add_scores(self, db_player: Player, scores: List[Score]):
        db_player.scores += scores

        self._db.commit_changes()
        Logger.log(db_player, f"Added {len(scores)} new scores")

    def add_score(self, player: Player, score: Score):
        player.scores.append(score)

        self._db.commit_changes()
        Logger.log(player, f"Added new {score}")

    def add_role(self, db_player, db_role):
        db_player.roles.append(db_role)

        self._db.commit_changes()
        Logger.log(db_player, f"Added {db_role}")

    def remove_role(self, db_player, db_role):
        db_player.roles.remove(db_role)

        self._db.commit_changes()
        Logger.log(db_player, f"Removed {db_role}")

    def remove_guild(self, db_player, db_guild):
        db_player.guilds.remove(db_guild)

        self._db.commit_changes()
        Logger.log(db_player, f"Removed {db_guild}")
