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
                func()

                attempting = False
            except Exception as e:
                attempt += 1
                error_handler(attempt, e)
                time.sleep(5)

    async def update_player(self, player):
        def update():
            new_player = self.uow.scoresaber.get_player(player.playerId)
            self.uow.player_repo.update_player(new_player)

        def error(attempt, e):
            Logger.log_add(f"Failed to get {player}, attempt: {attempt}, error: {e}")

        await self.__attempt(update, error)

    @tasks.loop(seconds=90)
    async def update_players(self, guild=None):
        start_time = time.process_time()

        if guild is None:
            players = self.uow.player_repo.get_players()
            Logger.log_add(f'Updating {len(players)} players')
        else:
            db_guild = self.uow.guild_repo.get_guild_by_id(guild.id)
            players = db_guild.players
            Logger.log_add(f'Updating {len(players)} players in {db_guild}')

        for player in players:
            await self.update_player(player)

        Logger.log_add(f"Update {len(players)} players in {time.process_time() - start_time} seconds")

    async def update_player_scores(self, player):
        def update():
            recent_scores = self.uow.scoresaber.get_recent_scores(player)
            self.uow.player_repo.add_scores(player.playerId, recent_scores)

            for recent_score in recent_scores:
                song = self.uow.beatsaver.get_song_by_score(recent_score)
                self.uow.score_repo.add_song(recent_score, song)

        def error(attempt, e):
            Logger.log_add(f"Failed to get {player} scores, attempt: {attempt}, error: {e}")

        await self.__attempt(update, error)

    @tasks.loop(seconds=60)
    async def update_players_scores(self, guild=None):
        start_time = time.process_time()

        if guild is None:
            players = self.uow.player_repo.get_players()
            Logger.log_add(f'Updating scores for {len(players)} players')
        else:
            db_guild = self.uow.guild_repo.get_guild_by_id(guild.id)
            players = db_guild.players
            Logger.log_add(f'Updating scores for {len(players)} players in {db_guild}')

        for player in players:
            await self.update_player_scores(player)

        Logger.log_add(f"Updated scores for {len(players)} players in {time.process_time() - start_time} seconds")

    async def mark_all_guild_scores_sent(self, guild):
        players = self.uow.guild_repo.get_players(guild)
        Logger.log_add(f"Marking all {len(players)} players scores as sent in {guild}")

        for player in players:
            await self.mark_all_player_scores_sent(player)

    async def mark_all_player_scores_sent(self, player):
        current_player = self.uow.player_repo.get_player_by_player_id(player.playerId)
        Logger.log_add(f"Marking all {player} scores sent")

        for guild in current_player.guilds:
            scores = self.uow.score_repo.get_unsent_scores(player, guild)

            for score in scores:
                self.uow.score_repo.mark_score_sent(score, guild)

    @tasks.loop(seconds=60)
    async def send_notifications(self, guild=None):
        start_time = time.process_time()

        if guild is None:
            players = self.uow.player_repo.get_players()
            Logger.log_add(f"Sending notifications for {len(players)} players")
        else:
            db_guild = self.uow.guild_repo.get_guild_by_id(guild.id)
            players = db_guild.players
            Logger.log_add(f"Sending notifications for {len(players)} players in {db_guild}")

        for player in players:
            for guild in player.guilds:
                if guild.recent_scores_channel_id is None:
                    Logger.log_add(f"{guild} is missing recent scores channel, skipping")
                    return

                channel = self.uow.client.get_channel(guild.recent_scores_channel_id)
                scores = self.uow.score_repo.get_unsent_scores(player, guild)

                Logger.log_add(f"{player} has {len(scores)} scores to notify at {guild}")

                for score in scores:
                    embed = Message.get_score_embed(player, score, score.song)
                    await channel.send(embed=embed)
                    self.uow.score_repo.mark_score_sent(score, guild)

        Logger.log_add(f"Sent all notifications in {time.process_time() - start_time} seconds")

    async def remove_player_roles(self, guild):
        start_time = time.process_time()

        db_guild = self.uow.guild_repo.get_guild_by_id(guild.id)
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
        start_time = time.process_time()

        if guild is None:
            db_guilds = self.uow.guild_repo.get_pp_guilds()
            Logger.log_add(f"Updating roles for {len(db_guilds)} guilds")
        else:
            db_guilds = [self.uow.guild_repo.get_guild_by_id(guild.id)]
            Logger.log_add(f"Updating roles for {db_guilds[0]}")

        for db_guild in db_guilds:
            for db_player in db_guild.players:
                await self.update_player_roles(db_guild, db_player)

        Logger.log_add(f"Updated roles for {len(db_guilds)} guilds in {time.process_time() - start_time} seconds")
