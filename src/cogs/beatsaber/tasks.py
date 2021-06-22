from discord.ext import tasks
from src.cogs.beatsaber.api.errors import NotFoundException
from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils
from src.cogs.beatsaber.leaderboard.guild_leaderboard import GuildLeaderboard
from src.cogs.beatsaber.message import Message
from src.log import Logger
from src.utils import Utils


class Tasks:

    def __init__(self, uow):
        self.uow = uow

    @tasks.loop(minutes=30)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players(self):
        db_players = self.uow.player_repo.get_players()
        Logger.log("task", f"Updating {len(db_players)} players")

        for db_player in db_players:
            self.update_player(db_player)

    def update_player(self, db_player):
        try:
            new_player = self.uow.scoresaber.get_player(db_player.playerId)

            self.uow.player_repo.update_player(new_player)
        except NotFoundException:
            Logger.log(db_player, "Could not find at ScoreSaber")

    @tasks.loop(minutes=2)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players_scores(self):
        db_players = self.uow.player_repo.get_players()
        Logger.log("task", f"Updating scores for {len(db_players)} players")

        for db_player in db_players:
            self.update_player_scores(db_player)

    def update_player_scores(self, db_player):
        try:
            recent_scores = self.uow.scoresaber.get_recent_scores(db_player.playerId)
            Logger.log(db_player, f"Got {len(recent_scores)} recent scores from ScoreSaber")

            # Add new scores to player
            self.uow.player_repo.add_scores(db_player, recent_scores)

            # Get db scores from recent scores
            db_scores = self.uow.score_repo.get_scores(recent_scores)

            # Update song for recent scores
            for db_score in db_scores:
                self.update_score_song(db_score)
        except NotFoundException:
            Logger.log(db_player, "Could not find scores on ScoreSaber")

    def update_score_song(self, db_score):
        if db_score.song is None:
            song = self.uow.song_repo.get_song_by_hash(db_score.songHash)

            if song is None:
                try:
                    song = self.uow.beatsaver.get_song_by_score(db_score)
                except NotFoundException:
                    Logger.log(db_score, "Could not find song on BeatSaver")

            self.uow.score_repo.add_song(db_score, song)

    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    async def send_notifications(self):
        db_players = self.uow.player_repo.get_players()
        Logger.log("task", f"Sending notifications for {len(db_players)} players")

        for db_player in db_players:
            for db_guild in db_player.guilds:
                await self.send_notification(db_guild, db_player)

    async def send_notification(self, db_guild, db_player):
        if db_guild.recent_scores_channel_id is None:
            Logger.log(db_guild, "Missing recent scores channel, skipping!")
            return

        channel = self.uow.bot.get_channel(db_guild.recent_scores_channel_id)
        db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

        Logger.log(db_guild, f"{db_player} has {len(db_scores)} scores to notify")

        # TODO LATER: ADD THINGY THAT CHECKS IF GUILD_SNIPES IN ENABLED FOR CURRENT GUILD
        guild_snipes = True

        for db_score in db_scores:
            if self.uow.score_repo.is_score_new(db_score):
                # Post as new score
                embed = Message.get_new_score_embed(db_player, db_score, db_score.song)
                await channel.send(embed=embed)

                self.uow.score_repo.mark_score_sent(db_score, db_guild)
            else:
                # Post as improvement
                previous_db_score = self.uow.score_repo.get_previous_score(db_score)

                embed = Message.get_improvement_score_embed(db_player, previous_db_score, db_score, db_score.song)
                await channel.send(embed=embed)
                self.uow.score_repo.mark_score_sent(db_score, db_guild)

            if guild_snipes:
                leaderboard = GuildLeaderboard(self.uow, db_guild, db_score.leaderboardId)

                if len(leaderboard.leaderboard_scores) > 0:
                    guild_leaderboard_embed = Message.get_leaderboard_embed(leaderboard.leaderboard_scores)
                    await channel.send(embed=guild_leaderboard_embed)

    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    async def update_all_player_roles(self):
        db_guilds = self.uow.guild_repo.get_guilds()
        Logger.log("task", f"Updating roles for {len(db_guilds)} guilds")

        for db_guild in db_guilds:
            await self.update_guild_roles(db_guild)

    async def update_guild_roles(self, db_guild):
        roles_class = BeatSaberUtils.get_enabled_roles(self.uow, db_guild)

        if len(roles_class) == 0:
            Logger.log("task", f"Skipping roles update for {db_guild}, no roles enabled!")
            return

        for db_player in db_guild.players:
            for update_role in roles_class:
                await update_role.update_player_role(db_player)
