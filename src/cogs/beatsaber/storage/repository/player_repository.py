from src.log import Logger
from src.cogs.beatsaber.storage.model.player import Player


class PlayerRepository:

    def __init__(self, database):
        self._db = database

    def add_to_guild(self, db_player, db_guild):
        db_player.guilds.append(db_guild)

        self._db.commit_changes()
        Logger.log(db_player, f"Added {db_guild}")

    def get_players(self):
        return self._db.session.query(Player).all()

    def get_player_by_player_id(self, player_id):
        return self._db.session.query(Player).filter(Player.playerId == player_id).first()

    def get_player_by_member_id(self, member_id):
        return self._db.session.query(Player).filter(Player.discord_user_id == member_id).first()

    def add_player(self, db_player):
        self._db.add_entry(db_player)

        return self.get_player_by_player_id(db_player.playerId)

    def remove_player(self, db_player):
        self._db.session.delete(db_player)

        self._db.commit_changes()
        Logger.log(db_player, "Deleted")

    def update_player(self, new_db_player):
        old_db_player = self.get_player_by_player_id(new_db_player.playerId)

        old_db_player.playerId = new_db_player.playerId
        old_db_player.playerName = new_db_player.playerName
        old_db_player.avatar = new_db_player.avatar
        old_db_player.rank = new_db_player.rank
        old_db_player.countryRank = new_db_player.countryRank
        old_db_player.pp = new_db_player.pp
        old_db_player.country = new_db_player.country
        old_db_player.role = new_db_player.role
        old_db_player.badges = new_db_player.badges
        old_db_player.history = new_db_player.history
        old_db_player.permissions = new_db_player.permissions
        old_db_player.inactive = new_db_player.inactive
        old_db_player.banned = new_db_player.banned

        self._db.commit_changes()
        Logger.log(old_db_player, "Updated")

    def add_scores(self, db_player, new_db_scores):
        new_score_list = []

        for new_score in new_db_scores:
            is_new = True

            for old_db_score in db_player.scores:
                if old_db_score.scoreId != new_score.scoreId:
                    continue

                if old_db_score.timeSet == new_score.timeSet:
                    is_new = False

            if is_new:
                new_score_list.append(new_score)

        db_player.scores += new_score_list

        self._db.commit_changes()
        Logger.log(db_player, f"Added {len(new_score_list)} new scores")

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
