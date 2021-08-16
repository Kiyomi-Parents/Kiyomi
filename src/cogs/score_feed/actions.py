from .errors import GuildRecentChannelExistsException, GuildRecentChannelNotFoundException
from .storage.model import SentScore
from .storage.uow import UnitOfWork
from .tasks import Tasks
from ..general.storage.model import Guild
from ..scoresaber.storage.model.player import Player
from ...log import Logger


class Actions:
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    def add_score_feed_channel(self, guild_id: int, channel_id: int):
        settings = self.uow.bot.get_cog("SettingsAPI")
        score_feed_channel_id = settings.get(guild_id, "score_feed_channel_id")

        if score_feed_channel_id is not None:
            guild = self.uow.bot.get_guild(guild_id)
            recent_scores_channel = guild.get_channel(score_feed_channel_id)

            raise GuildRecentChannelExistsException(f"Channel **{recent_scores_channel.name}** has already been set as the notification channel!")

        settings.set(guild_id, "score_feed_channel_id", channel_id)

        self.mark_all_guild_scores_sent(guild_id)

    def remove_score_feed_channel(self, guild_id):
        settings = self.uow.bot.get_cog("SettingsAPI")
        score_feed_channel_id = settings.get(guild_id, "score_feed_channel_id")

        if score_feed_channel_id is None:
            raise GuildRecentChannelNotFoundException("There isn't a notification channel set for this Discord server.")

        settings.delete(guild_id, "score_feed_channel_id")

    def mark_all_guild_scores_sent(self, guild_id: int):
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")
        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        Logger.log(guild_players[0].guild, f"Marking scores sent for {len(guild_players)} players")

        for guild_player in guild_players:
            self.mark_player_scores_sent(guild_player.player, guild_player.guild)

    def mark_all_player_scores_sent(self, player: Player):
        Logger.log(player, "Marking all scores as sent")

        for guild in player.guilds:
            self.mark_player_scores_sent(player, guild)

    def mark_player_scores_sent(self, player: Player, guild: Guild):
        Logger.log(player, f"Marking all scores as sent in {guild}")

        scores = self.tasks.get_unsent_scores(player, guild)

        sent_scores = []
        for score in scores:
            sent_scores.append(SentScore(score.id, guild.id))

        self.uow.sent_score_repo.add_all(sent_scores)

    async def send_notifications(self, guild_id: int):
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")
        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        Logger.log(guild_players[0].guild, f"Sending notifications for {len(guild_players)} players")

        for guild_player in guild_players:
            await self.tasks.send_notification(guild_player.guild, guild_player.player)
