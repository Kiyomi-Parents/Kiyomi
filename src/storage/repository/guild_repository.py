from src.log import Logger
from src.storage.model.discord_guild import DiscordGuild


class GuildRepository:

    def __init__(self, database):
        self._db = database

    def get_guilds(self):
        return self._db.session.query(DiscordGuild).all()

    def get_pp_guilds(self):
        return self._db.session.query(DiscordGuild).filter(DiscordGuild.pp_roles).all()

    def get_guild_by_id(self, guild_id):
        return self._db.session.query(DiscordGuild).filter(DiscordGuild.discord_guild_id == guild_id).first()

    def add_guild(self, guild):
        guild = DiscordGuild(guild)
        self._db.add_entry(guild)

    def set_recent_score_channel_id(self, guild_id, channel_id):
        discord_guild = self.get_guild_by_id(guild_id)

        discord_guild.recent_scores_channel_id = channel_id

        self._db.commit_changes()
        Logger.log_add(f"Updated {discord_guild} recent scores channel to {channel_id}")

    def add_player(self, guild_id, player):
        discord_guild = self.get_guild_by_id(guild_id)

        discord_guild.players.append(player)

        self._db.commit_changes()
        Logger.log_add(f"Added {player} to {discord_guild}")

    def remove_player(self, guild_id, player):
        discord_guild = self.get_guild_by_id(guild_id)

        discord_guild.players.remove(player)

        self._db.commit_changes()
        Logger.log_add(f"Removed {player} from {discord_guild}")

    def get_players(self, guild):
        discord_guild = self.get_guild_by_id(guild.discord_guild_id)

        return discord_guild.players

    def set_feature(self, guild_id, feature_flag, status):
        discord_guild = self.get_guild_by_id(guild_id)

        if feature_flag == "ppRoles":
            discord_guild.pp_roles = status

        self._db.commit_changes()
        Logger.log_add(f"Set {feature_flag} on {discord_guild} to {status}")

    def add_role(self, guild_id, role):
        discord_guild = self.get_guild_by_id(guild_id)

        discord_guild.roles.append(role)

        self._db.commit_changes()
        Logger.log_add(f"Added {role} to {discord_guild}")

    def remove_role(self, guild_id, role):
        discord_guild = self.get_guild_by_id(guild_id)

        discord_guild.roles.remove(role)

        self._db.commit_changes()
        Logger.log_add(f"Removed {role} from {discord_guild}")
