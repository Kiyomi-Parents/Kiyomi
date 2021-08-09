from typing import List

from src.cogs.beatsaber.storage.model.player import Player
from src.cogs.beatsaber.storage.model.score import Score
from src.log import Logger
from src.utils import Utils


class PlayerRepository:

    def __init__(self, database):
        self._db = database

    def add_to_guild(self, db_player, db_guild):
        db_player.guilds.append(db_guild)

        self._db.commit_changes()
        Logger.log(db_player, f"Added {db_guild}")

    def get_players(self):
        return self._db.session.query(Player).all()

    def get_player_by_internal_player_id(self, internal_player_id):
        return self._db.session.query(Player).filter(Player.id == internal_player_id).first()

    def get_player_by_player_id(self, player_id):
        return self._db.session.query(Player).filter(Player.player_id == player_id).first()

    def get_player_by_member_id(self, member_id):
        return self._db.session.query(Player).filter(Player.discord_user_id == member_id).first()

    def add_player(self, db_player):
        self._db.add_entry(db_player)

        return self.get_player_by_player_id(db_player.player_id)

    def remove_player(self, db_player):
        self._db.session.delete(db_player)

        self._db.commit_changes()
        Logger.log(db_player, "Deleted")

    def update_player(self, new_db_player: Player):
        old_db_player = self.get_player_by_player_id(new_db_player.player_id)

        Utils.update_class(old_db_player, new_db_player)

        self._db.commit_changes()
        Logger.log(old_db_player, "Updated")

    def add_scores(self, db_player: Player, scores: List[Score]):
        db_player.scores += scores

        self._db.commit_changes()
        Logger.log(db_player, f"Added {len(scores)} new scores")

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
