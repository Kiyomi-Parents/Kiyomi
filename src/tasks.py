import time

from discord.ext import tasks

from src.api.errors import *
from src.log import Logger
from src.message import Message
from src.roles import Roles
from src.utils import Utils


class Tasks:

    def __init__(self, uow):
        self.uow = uow

    @tasks.loop(seconds=90)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players(self, guild=None):
        if guild is None:
            db_players = self.uow.player_repo.get_players()
            Logger.log("task", f'Updating {len(db_players)} players')
        else:
            db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
            db_players = db_guild.players
            Logger.log(db_guild, f'Updating {len(db_players)} players')

        for db_player in db_players:
            self.update_player(db_player)

    def update_player(self, db_player):
        try:
            new_player = self.uow.scoresaber.get_player(db_player.playerId)

            self.uow.player_repo.update_player(new_player)
        except NotFound:
            Logger.log(db_player, f"Could not find at ScoreSaber")

    @tasks.loop(seconds=60)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players_scores(self, guild=None):
        if guild is None:
            db_players = self.uow.player_repo.get_players()
            Logger.log("task", f'Updating scores for {len(db_players)} players')
        else:
            db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
            db_players = db_guild.players
            Logger.log(db_guild, f'Updating scores for {len(db_players)} players')

        for db_player in db_players:
            self.update_player_scores(db_player)

    def update_player_scores(self, db_player):
        try:
            recent_scores = self.uow.scoresaber.get_recent_scores(db_player)

            # Add new scores to player
            self.uow.player_repo.add_scores(db_player, recent_scores)

            # Update existing scores
            self.uow.score_repo.update_scores(recent_scores)

            # Get db scores from recent scores
            db_scores = self.uow.score_repo.get_scores(recent_scores)

            # Update song for recent scores
            for db_score in db_scores:
                self.update_score_song(db_score)
        except NotFound:
            Logger.log(db_player, f"Could not find scores on ScoreSaber")

    def update_scores_song(self):
        db_scores = self.uow.score_repo.get_scores_without_song()

        if len(db_scores) == 0:
            Logger.log("task", f"No song updates needed for scores")
            return

        Logger.log("task", f'Updating songs for {len(db_scores)} scores')

        for db_score in db_scores:
            self.update_score_song(db_score)

        Logger.log("task", f"Updated songs for {len(db_scores)} scores")

    def update_score_song(self, db_score):
        if db_score.song is None:
            song = self.uow.song_repo.get_song_by_hash(db_score.songHash)

            if song is None:
                try:
                    song = self.uow.beatsaver.get_song_by_score(db_score)
                except NotFound:
                    Logger.log(db_score, f"Could not find song on BeatSaver")

            self.uow.score_repo.add_song(db_score, song)

    @tasks.loop(seconds=10)
    @Utils.time_task
    @Utils.discord_ready
    async def send_notifications(self, guild=None):
        if guild is None:
            db_players = self.uow.player_repo.get_players()
            Logger.log("task", f"Sending notifications for {len(db_players)} players")
        else:
            db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
            db_players = db_guild.players
            Logger.log(db_guild, f"Sending notifications for {len(db_players)} players")

        for db_player in db_players:
            for db_guild in db_player.guilds:
                if db_guild.recent_scores_channel_id is None:
                    Logger.log(db_guild, f"Missing recent scores channel, skipping!")
                    continue

                channel = self.uow.client.get_channel(db_guild.recent_scores_channel_id)
                db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

                Logger.log(db_guild, f"{db_player} has {len(db_scores)} scores to notify")

                for db_score in db_scores:
                    embed = Message.get_score_embed(db_player, db_score, db_score.song)
                    await channel.send(embed=embed)
                    self.uow.score_repo.mark_score_sent(db_score, db_guild)

    def mark_all_guild_scores_sent(self, db_guild):
        Logger.log(db_guild, f"Marking scores sent for {len(db_guild.players)} players")

        for db_player in db_guild.players:
            self.mark_player_scores_sent(db_player, db_guild)

    def mark_all_player_scores_sent(self, db_player):
        Logger.log(db_player, f"Marking all scores as sent")

        for db_guild in db_player.guilds:
            self.mark_player_scores_sent(db_player, db_guild)

    def mark_player_scores_sent(self, db_player, db_guild):
        Logger.log(db_player, f"Marking all scores as sent in {db_guild}")

        db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

        for db_score in db_scores:
            self.uow.score_repo.mark_score_sent(db_score, db_guild)

    @tasks.loop(seconds=90)
    @Utils.time_task
    @Utils.discord_ready
    async def update_all_player_roles(self, guild=None):
        if guild is None:
            db_guilds = self.uow.guild_repo.get_pp_guilds()
            Logger.log("task", f"Updating roles for {len(db_guilds)} guilds")
        else:
            db_guilds = [self.uow.guild_repo.get_guild_by_discord_id(guild.id)]
            Logger.log(db_guilds[0], f"Updating roles")

        for db_guild in db_guilds:
            for db_player in db_guild.players:
                await self.update_player_roles(db_guild, db_player)

    async def update_player_roles(self, db_guild, db_player):
        roles = Roles(self.uow, db_guild, db_player)
        role = await roles.get_pp_role()

        try:
            await roles.give_member_role(role)
            await roles.remove_obsolete_player_roles()
        except Exception as e:
            Logger.log_add(f'Exception {e} in update_player_roles')

    async def remove_player_roles(self, db_guild, db_player):
        roles = Roles(self.uow, db_guild, db_player)

        await roles.remove_player_roles()

    async def remove_guild_roles(self, guild):
        db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
        Logger.log(db_guild, f"Removing roles")

        for db_player in db_guild.players:
            roles = Roles(self.uow, db_guild, db_player)
            await roles.remove_player_roles()
            await roles.remove_guild_roles()
