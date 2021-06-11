from src.api import NotFoundException
from src.commands.beatsaber.beatsaber_utils import BeatSaberUtils
from src.commands.beatsaber.feature.feature import FeatureFlagNotFoundException


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
            raise PlayerExistsException(f'Player **{db_player.playerName}** has already been added!')

        # Add new player to db if not found
        if db_player is None:
            try:
                new_player = self.uow.scoresaber.get_player(scoresaber_id)
                new_player.discord_user_id = member_id

                self.uow.player_repo.add_player(new_player)
            except NotFoundException:
                raise PlayerNotFoundException(f"Could not find player!")

            db_player = self.uow.player_repo.get_player_by_member_id(member_id)

        self.uow.player_repo.add_to_guild(db_player, db_guild)

        # Get player scores and marked them sent to decrease spam
        self.tasks.update_player_scores(db_player)
        self.tasks.mark_all_player_scores_sent(db_player)

        # Add role to player
        await self.update_player_roles(db_guild, db_player)

        return db_player

    async def remove_player(self, guild_id, member_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        db_player = self.uow.player_repo.get_player_by_member_id(member_id)

        if db_player is None:
            raise PlayerNotFoundException(f"You don't have a ScoreSaber profile linked to yourself.")

        if db_guild is None:
            raise GuildNotFoundException(f"Your ScoreSaber profile isn't linked to this Discord server.")

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

    def add_recent_channel(self, guild_id, channel_id):
        guild = self.uow.bot.get_guild(guild_id)
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        if db_guild is None:
            raise GuildNotFoundException(f"Could not find guild with ID: {guild_id}")

        if db_guild.recent_scores_channel_id is not None:
            recent_scores_channel = guild.get_channel(db_guild.recent_scores_channel_id)

            raise GuildRecentChannelExistsException(
                f"Channel **{recent_scores_channel.name}** has already been set as the notification channel!")

        self.uow.guild_repo.set_recent_score_channel_id(db_guild, channel_id)
        self.tasks.mark_all_guild_scores_sent(db_guild)

    def remove_recent_channel(self, guild_id):
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        if db_guild.recent_scores_channel_id is None:
            raise GuildRecentChannelNotFoundException(
                f"There isn't a notification channel set for this Discord server.")

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
