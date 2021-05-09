from src.log import Logger
from src.storage.model.player import Player


class PlayerRepository:

    def __init__(self, database):
        self._db = database

    def add_to_guild(self, playerId, guild):
        player = self.get_player_by_player_id(playerId)

        player.guilds.append(guild)

        self._db.commit_changes()
        Logger.log_add(f"Added {player} to {guild}")

    def get_players(self):
        return self._db.session.query(Player).all()

    def get_player_by_player_id(self, playerId):
        return self._db.session.query(Player).filter(Player.playerId == playerId).first()

    def add_player(self, player):
        self._db.add_entry(player)

    def update_player(self, new_player):
        old_player = self.get_player_by_player_id(new_player.playerId)

        old_player.playerId = new_player.playerId
        old_player.playerName = new_player.playerName
        old_player.avatar = new_player.avatar
        old_player.rank = new_player.rank
        old_player.countryRank = new_player.countryRank
        old_player.pp = new_player.pp
        old_player.country = new_player.country
        old_player.role = new_player.role
        old_player.badges = new_player.badges
        old_player.history = new_player.history
        old_player.permissions = new_player.permissions
        old_player.inactive = new_player.inactive
        old_player.banned = new_player.banned

        self._db.commit_changes()
        Logger.log_add(f"Updated {old_player}")

    def add_scores(self, playerId, new_scores):
        player = self.get_player_by_player_id(playerId)

        new_score_list = []

        for new_score in new_scores:
            is_new = True

            for old_score in player.scores:
                if old_score.scoreId == new_score.scoreId:
                    is_new = False

            if is_new:
                new_score_list.append(new_score)

        player.scores += new_score_list

        self._db.commit_changes()
        Logger.log_add(f"Added {len(new_score_list)} new scores to {player}")

    def add_role(self, player, role):
        player = self.get_player_by_player_id(player.playerId)

        player.roles.append(role)

        self._db.commit_changes()
        Logger.log_add(f"Added {role} to {player}")

    def remove_role(self, player, role):
        player = self.get_player_by_player_id(player.playerId)

        player.roles.remove(role)

        self._db.commit_changes()
        Logger.log_add(f"Removed {role} from {player}")
