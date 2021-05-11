from src.log import Logger
from src.storage.model.discord_guild import DiscordGuild


class GuildRepository:

    def __init__(self, database):
        self._db = database

    def get_guilds(self):
        return self._db.session.query(DiscordGuild).all()

    def get_pp_guilds(self):
        return self._db.session.query(DiscordGuild).filter(DiscordGuild.pp_roles).all()

    def get_guild_by_discord_id(self, guild_id):
        return self._db.session.query(DiscordGuild).filter(DiscordGuild.discord_guild_id == guild_id).first()

    def add_guild(self, guild):
        guild = DiscordGuild(guild)
        self._db.add_entry(guild)

    def set_recent_score_channel_id(self, db_guild, channel_id):
        db_guild.recent_scores_channel_id = channel_id

        self._db.commit_changes()
        Logger.log_add(f"Updated {db_guild} recent scores channel to {channel_id}")

    def add_player(self, db_guild, db_player):
        db_guild.players.append(db_player)

        self._db.commit_changes()
        Logger.log_add(f"Added {db_player} to {db_guild}")

    def remove_player(self, db_guild, db_player):
        db_guild.players.remove(db_player)

        self._db.commit_changes()
        Logger.log_add(f"Removed {db_player} from {db_guild}")

    def set_feature(self, db_guild, feature_flag, status):
        if feature_flag == "ppRoles":
            db_guild.pp_roles = status

        self._db.commit_changes()
        Logger.log_add(f"Set {feature_flag} on {db_guild} to {status}")

    def add_role(self, db_guild, db_role):
        db_guild.roles.append(db_role)

        self._db.commit_changes()
        Logger.log_add(f"Added {db_role} to {db_guild}")

    def remove_role(self, db_guild, db_role):
        db_guild.roles.remove(db_role)

        self._db.commit_changes()
        Logger.log_add(f"Removed {db_role} from {db_guild}")
