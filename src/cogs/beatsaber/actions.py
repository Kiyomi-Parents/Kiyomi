from src.api import NotFoundException
from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils
from src.cogs.beatsaber.feature.feature import FeatureFlagNotFoundException
from src.cogs.beatsaber.leaderboard.guild_leaderboard import GuildLeaderboard
from src.log import Logger


class PlayerExistsException(Exception):
    pass


class PlayerNotFoundException(Exception):
    pass


class GuildNotFoundException(Exception):
    pass


class GuildRecentChannelExistsException(Exception):
    pass


class GuildRecentChannelNotFoundException(Exception):
    pass


class SongNotFound(Exception):
    pass


class Actions:
    def __init__(self, uow, tasks):
        self.uow = uow
        self.tasks = tasks

    async def add_player(self, guild_id, member_id, scoresaber_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        db_player = self.uow.player_repo.get_player_by_member_id(member_id)

        if db_guild is None:
            raise GuildNotFoundException(f"Failed to find {guild_id}")

        if db_player is not None and db_player in db_guild.players:
            raise PlayerExistsException(f"Player **{db_player.playerName}** has already been added!")

        # Add new player to db if not found
        if db_player is None:
            try:
                new_player = self.uow.scoresaber.get_player(scoresaber_id)
                new_player.discord_user_id = member_id

                self.uow.player_repo.add_player(new_player)
            except NotFoundException as error:
                raise PlayerNotFoundException("Could not find player!") from error

            db_player = self.uow.player_repo.get_player_by_member_id(member_id)

        self.uow.player_repo.add_to_guild(db_player, db_guild)

        # Get player scores and marked them sent to decrease spam
        self.tasks.update_player_scores(db_player)
        self.mark_all_player_scores_sent(db_player)

        # Add role to player
        await self.update_player_roles(db_guild, db_player)

        return db_player

    async def remove_player(self, guild_id, member_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        db_player = self.uow.player_repo.get_player_by_member_id(member_id)

        if db_player is None:
            raise PlayerNotFoundException("You don't have a ScoreSaber profile linked to yourself.")

        if db_guild is None:
            raise GuildNotFoundException("Your ScoreSaber profile isn't linked to this Discord server.")

        self.uow.player_repo.remove_guild(db_player, db_guild)

        # Remove player roles
        await self.remove_player_roles(db_guild, db_player)

        # If player doesnt belong to any guilds, remove player
        if len(db_player.guilds) == 0:
            self.uow.player_repo.remove_player(db_player)

        return db_player

    async def update_player_roles(self, db_guild, db_player):
        roles_class = BeatSaberUtils.get_enabled_roles(self.uow, db_guild)

        for role_class in roles_class:
            await role_class.assign_player_role(db_player)

    async def remove_player_roles(self, db_guild, db_player):
        roles_class = BeatSaberUtils.get_enabled_roles(self.uow, db_guild)

        for role_class in roles_class:
            await role_class.strip_player_role(db_player)

    def mark_all_guild_scores_sent(self, db_guild):
        Logger.log(db_guild, f"Marking scores sent for {len(db_guild.players)} players")

        for db_player in db_guild.players:
            self.mark_player_scores_sent(db_player, db_guild)

    def mark_all_player_scores_sent(self, db_player):
        Logger.log(db_player, "Marking all scores as sent")

        for db_guild in db_player.guilds:
            self.mark_player_scores_sent(db_player, db_guild)

    def mark_player_scores_sent(self, db_player, db_guild):
        Logger.log(db_player, f"Marking all scores as sent in {db_guild}")

        db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

        for db_score in db_scores:
            self.uow.score_repo.mark_score_sent(db_score, db_guild)

    def add_recent_channel(self, guild_id, channel_id):
        guild = self.uow.bot.get_guild(guild_id)
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        if db_guild is None:
            raise GuildNotFoundException(f"Could not find guild with ID: {guild_id}")

        if db_guild.recent_scores_channel_id is not None:
            recent_scores_channel = guild.get_channel(db_guild.recent_scores_channel_id)

            raise GuildRecentChannelExistsException(f"Channel **{recent_scores_channel.name}** has already been set as the notification channel!")

        self.uow.guild_repo.set_recent_score_channel_id(db_guild, channel_id)
        self.mark_all_guild_scores_sent(db_guild)

    def remove_recent_channel(self, guild_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        if db_guild.recent_scores_channel_id is None:
            raise GuildRecentChannelNotFoundException("There isn't a notification channel set for this Discord server.")

        self.uow.guild_repo.set_recent_score_channel_id(db_guild, None)

    async def enable_feature(self, guild_id, feature_flag):
        feature_class = BeatSaberUtils.get_feature(feature_flag)

        if feature_class is None:
            raise FeatureFlagNotFoundException(f"Could not find feature flag: {feature_flag}")

        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        feature = feature_class(self.uow, db_guild)

        await feature.set(True)

    async def disable_feature(self, guild_id, feature_flag):
        feature_class = BeatSaberUtils.get_feature(feature_flag)

        if feature_class is None:
            raise FeatureFlagNotFoundException(f"Could not find feature flag: {feature_flag}")

        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        feature = feature_class(self.uow, db_guild)

        await feature.set(False)

    async def update_players(self, guild_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        Logger.log(db_guild, f"Updating {len(db_guild.players)} players")

        for db_player in db_guild.players:
            self.tasks.update_player(db_player)

    async def update_players_scores(self, guild_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        Logger.log(db_guild, f"Updating scores for {len(db_guild.players)} players")

        for db_player in db_guild.players:
            self.tasks.update_player_scores(db_player)

    async def send_notifications(self, guild_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        Logger.log(db_guild, f"Sending notifications for {len(db_guild.players)} players")

        for db_player in db_guild.players:
            await self.tasks.send_notification(db_guild, db_player)

    async def update_all_player_roles(self, guild_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        Logger.log(db_guild, f"Updating roles for {len(db_guild.players)} players")
        await self.tasks.update_guild_roles(db_guild)

    async def get_song(self, song_key):
        db_song = self.uow.song_repo.get_song_by_key(song_key)

        if db_song is None:
            try:
                db_song = self.uow.beatsaver.get_song_by_key(song_key)
                self.uow.song_repo.add_song(db_song)
            except NotFoundException as error:
                raise SongNotFound(f"Could not find song with key {song_key}") from error

        return db_song

    async def get_guild_leaderboard(self, guild_id, song_key):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        db_song = await self.get_song(song_key)
        leaderboard_id = self.uow.score_repo.get_leaderboard_id_by_hash(db_song.hash)

        leaderboard = GuildLeaderboard(self.uow, db_guild, leaderboard_id)

        return leaderboard.leaderboard_scores
