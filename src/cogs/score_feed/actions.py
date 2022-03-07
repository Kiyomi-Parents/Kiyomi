from .errors import GuildRecentChannelExistsException, GuildRecentChannelNotFoundException
from .storage.model import SentScore
from .storage.uow import UnitOfWork
from .tasks import Tasks
from src.cogs.general.storage.model import Guild
from src.cogs.scoresaber.storage.model.player import Player
from src.log import Logger


class Actions:
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

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
        scores = self.uow.sent_score_repo.get_unsent_scores(guild.id, player.id)

        Logger.log(player, f"Marking {len(scores)} scores as sent in {guild}")

        sent_scores = []
        for score in scores:
            sent_scores.append(SentScore(score.id, guild.id))

        if len(sent_scores) != 0:
            self.uow.sent_score_repo.add_all(sent_scores)

    async def send_notifications(self, guild_id: int):
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")
        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        Logger.log(guild_players[0].guild, f"Sending notifications for {len(guild_players)} players")

        for guild_player in guild_players:
            await self.tasks.send_notification(guild_player.guild, guild_player.player)
