import time

from discord.ext import tasks

from src.log import Logger
from src.message import Message
from src.roles import Roles


class Tasks:

    def __init__(self, uow):
        self.uow = uow

    @staticmethod
    async def __attempt(func, error_handler):
        attempt = 0
        attempting = True

        while attempting and attempt < 6:
            try:
                await func()

                attempting = False
            except Exception as e:
                attempt += 1
                error_handler(attempt, e)
                time.sleep(5)

    async def update_player(self, db_player):
        async def update():
            new_player = self.uow.scoresaber.get_player(db_player.playerId)
            self.uow.player_repo.update_player(new_player)

        def error(attempt, e):
            Logger.log_add(f"Failed to get {db_player}, attempt: {attempt}, error: {e}")

        await self.__attempt(update, error)

    @tasks.loop(seconds=90)
    async def update_players(self, guild=None):
        if not self.uow.client.is_ready():
            Logger.log_add("Discord client not ready, skipping task update players")
            return

        start_time = time.process_time()

        if guild is None:
            db_players = self.uow.player_repo.get_players()
            Logger.log_add(f'Updating {len(db_players)} players')
        else:
            db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
            db_players = db_guild.players
            Logger.log_add(f'Updating {len(db_players)} players in {db_guild}')

        for db_player in db_players:
            await self.update_player(db_player)

        Logger.log_add(f"Update {len(db_players)} players in {time.process_time() - start_time} seconds")

    async def update_player_scores(self, db_player):
        async def update():
            recent_scores = self.uow.scoresaber.get_recent_scores(db_player)
            self.uow.player_repo.add_scores(db_player, recent_scores)

            await self.update_scores_song()

            self.uow.score_repo.update_scores(recent_scores)

        def error(attempt, e):
            Logger.log_add(f"Failed to get {db_player} scores, attempt: {attempt}, error: {e}")

        await self.__attempt(update, error)

    @tasks.loop(seconds=60)
    async def update_players_scores(self, guild=None):
        if not self.uow.client.is_ready():
            Logger.log_add("Discord client not ready, skipping task update player scores")
            return

        start_time = time.process_time()

        if guild is None:
            db_players = self.uow.player_repo.get_players()
            Logger.log_add(f'Updating scores for {len(db_players)} players')
        else:
            db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
            db_players = db_guild.players
            Logger.log_add(f'Updating scores for {len(db_players)} players in {db_guild}')

        for db_player in db_players:
            await self.update_player_scores(db_player)

        Logger.log_add(f"Updated scores for {len(db_players)} players in {time.process_time() - start_time} seconds")

    async def update_score_song(self, db_score):
        if db_score.song is None:
            song = self.uow.song_repo.get_song_by_hash(db_score.songHash)

            if song is None:
                song = self.uow.beatsaver.get_song_by_score(db_score)

            self.uow.score_repo.add_song(db_score, song)

    async def update_scores_song(self):
        db_scores = self.uow.score_repo.get_scores_without_song()

        if len(db_scores) == 0:
            Logger.log_add(f"No song updates needed for scores")
            return

        Logger.log_add(f'Updating songs for {len(db_scores)} scores')

        for db_score in db_scores:
            await self.update_score_song(db_score)

        Logger.log_add(f"Updated songs for {len(db_scores)} scores")

    async def mark_all_guild_scores_sent(self, db_guild):
        Logger.log_add(f"Marking all {len(db_guild.players)} players scores as sent in {db_guild}")

        for db_player in db_guild.players:
            await self.mark_all_player_scores_sent(db_player)

    async def mark_all_player_scores_sent(self, db_player):
        Logger.log_add(f"Marking all {db_player} scores sent")

        for db_guild in db_player.guilds:
            db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

            for db_score in db_scores:
                self.uow.score_repo.mark_score_sent(db_score, db_guild)

    @tasks.loop(seconds=10)
    async def send_notifications(self, guild=None):
        if not self.uow.client.is_ready():
            Logger.log_add("Discord client not ready, skipping task send notifications")
            return

        start_time = time.process_time()

        if guild is None:
            db_players = self.uow.player_repo.get_players()
            Logger.log_add(f"Sending notifications for {len(db_players)} players")
        else:
            db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
            db_players = db_guild.players
            Logger.log_add(f"Sending notifications for {len(db_players)} players in {db_guild}")

        for db_player in db_players:
            for db_guild in db_player.guilds:
                if db_guild.recent_scores_channel_id is None:
                    Logger.log_add(f"{db_guild} is missing recent scores channel, skipping")
                    return

                channel = self.uow.client.get_channel(db_guild.recent_scores_channel_id)
                db_scores = self.uow.score_repo.get_unsent_scores(db_player, db_guild)

                Logger.log_add(f"{db_player} has {len(db_scores)} scores to notify at {db_guild}")

                for db_score in db_scores:
                    embed = Message.get_score_embed(db_player, db_score, db_score.song)
                    await channel.send(embed=embed)
                    self.uow.score_repo.mark_score_sent(db_score, db_guild)

        Logger.log_add(f"Sent all notifications in {time.process_time() - start_time} seconds")

    async def remove_player_roles(self, db_guild, db_player):
        roles = Roles(self.uow, db_guild, db_player)

        await roles.remove_player_roles()

    async def remove_guild_roles(self, guild):
        start_time = time.process_time()

        db_guild = self.uow.guild_repo.get_guild_by_discord_id(guild.id)
        Logger.log_add(f"Removing roles for {db_guild}")

        for db_player in db_guild.players:
            roles = Roles(self.uow, db_guild, db_player)
            await roles.remove_player_roles()
            await roles.remove_guild_roles()

        Logger.log_add(f"Removed roles for {db_guild} guilds in {time.process_time() - start_time} seconds")

    async def update_player_roles(self, db_guild, db_player):
        roles = Roles(self.uow, db_guild, db_player)
        role = await roles.get_pp_role()

        await roles.give_member_role(role)
        await roles.remove_obsolete_player_roles()

    @tasks.loop(seconds=90)
    async def update_all_player_roles(self, guild=None):
        if not self.uow.client.is_ready():
            Logger.log_add("Discord client not ready, skipping task update all player roles")
            return

        start_time = time.process_time()

        if guild is None:
            db_guilds = self.uow.guild_repo.get_pp_guilds()
            Logger.log_add(f"Updating roles for {len(db_guilds)} guilds")
        else:
            db_guilds = [self.uow.guild_repo.get_guild_by_discord_id(guild.id)]
            Logger.log_add(f"Updating roles for {db_guilds[0]}")

        for db_guild in db_guilds:
            for db_player in db_guild.players:
                await self.update_player_roles(db_guild, db_player)

        Logger.log_add(f"Updated roles for {len(db_guilds)} guilds in {time.process_time() - start_time} seconds")
