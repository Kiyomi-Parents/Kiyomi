import asyncio

import pybeatsaver
import pyscoresaber
from discord.ext import tasks

from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils
from src.cogs.beatsaber.leaderboard.guild_leaderboard import GuildLeaderboard
from src.cogs.beatsaber.message import Message
from src.cogs.beatsaber.storage.model.beatmap import Beatmap
from src.cogs.beatsaber.storage.model.player import Player
from src.cogs.beatsaber.storage.model.score import Score
from src.log import Logger
from src.utils import Utils


class Tasks:

    def __init__(self, uow):
        self.uow = uow
        self.update_players_lock = asyncio.Lock()
        self.update_players_scores_lock = asyncio.Lock()
        self.send_notifications_lock = asyncio.Lock()
        self.update_all_player_roles_lock = asyncio.Lock()

    @tasks.loop(minutes=30)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players(self):
        async with self.update_players_lock:
            db_players = self.uow.player_repo.get_players()
            Logger.log("task", f"Updating {len(db_players)} players")

            for db_player in db_players:
                self.update_player(db_player)

    def update_player(self, db_player: Player):
        try:
            new_player = self.uow.scoresaber.get_player_basic(db_player.playerId)
            player = Player(new_player)

            self.uow.player_repo.update_player(player)
        except pyscoresaber.NotFoundException:
            Logger.log(db_player, "Could not find at ScoreSaber")

    @tasks.loop(minutes=2)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players_scores(self):
        async with self.update_players_scores_lock:
            db_players = self.uow.player_repo.get_players()
            Logger.log("task", f"Updating scores for {len(db_players)} players")

            for db_player in db_players:
                self.update_player_scores(db_player)

    def update_player_scores(self, db_player: Player):
        try:
            recent_scores = self.uow.scoresaber.get_recent_scores(db_player.playerId)
            Logger.log(db_player, f"Got {len(recent_scores)} recent scores from ScoreSaber")

            # Filter out already existing scores
            new_scores = []

            for recent_score in recent_scores:
                new_score = Score(recent_score)

                if self.uow.score_repo.is_score_new(new_score):
                    new_scores.append(new_score)

            # Add new scores to player
            self.uow.player_repo.add_scores(db_player, new_scores)

            # Get db scores from recent scores
            db_scores = self.uow.score_repo.get_scores(new_scores)

            # Update song for recent scores
            for db_score in db_scores:
                self.update_score_song(db_score)

        except pyscoresaber.NotFoundException:
            Logger.log(db_player, "Could not find scores on ScoreSaber")

    def update_score_song(self, score: Score):
        if score.beatmap_version is None:
            beatmap = self.uow.beatmap_repo.get_beatmap_by_hash(score.songHash)

            if beatmap is None:
                try:
                    map_detail = self.uow.beatsaver.get_map_by_hash(score.songHash)
                    beatmap = Beatmap(map_detail)
                    self.uow.beatmap_repo.add_beatmap(beatmap)

                    self.uow.score_repo.add_beatmap(score, beatmap)
                except pybeatsaver.NotFoundException:
                    Logger.log(score, "Could not find song on BeatSaver")


    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    async def send_notifications(self):
        async with self.send_notifications_lock:
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

        if channel is None:
            Logger.log(db_guild, "Recent scores channel not found, skipping!")
            return

        db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

        Logger.log(db_guild, f"{db_player} has {len(db_scores)} scores to notify")

        score_repo = self.uow.score_repo
        for db_score in db_scores:
            previous_db_score = score_repo.get_previous_score(db_score)

            if previous_db_score is None:
                # Post as new score
                embed = Message.get_new_score_embed(db_player, db_score, db_score.song)
                await channel.send(embed=embed)

                score_repo.mark_score_sent(db_score, db_guild)
            else:
                # Post as improvement
                previous_db_score = score_repo.update_score_pp_weight(previous_db_score, self.uow.player_repo)
                embed = Message.get_improvement_score_embed(db_player, previous_db_score, db_score, db_score.song)
                await channel.send(embed=embed)

                score_repo.mark_score_sent(db_score, db_guild)

            # Guild snipes leaderboard
            if db_guild.guild_snipes:
                leaderboard = GuildLeaderboard(self.uow, db_guild, db_score.leaderboardId)

                if len(leaderboard.leaderboard_scores) > 0:
                    guild_leaderboard_embed = Message.get_leaderboard_embed(leaderboard.get_top_scores(3))
                    await channel.send(embed=guild_leaderboard_embed)

    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    async def update_all_player_roles(self):
        async with self.update_all_player_roles_lock:
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
