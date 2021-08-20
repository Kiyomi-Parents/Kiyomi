import asyncio
from typing import List

from discord.ext import tasks

from src.log import Logger
from src.utils import Utils
from .message import Message
from .storage.model import SentScore
from .storage.uow import UnitOfWork
from src.cogs.general.storage.model import Guild
from src.cogs.scoresaber.storage.model.player import Player
from src.cogs.scoresaber.storage.model.score import Score


class Tasks:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.send_notifications_lock = asyncio.Lock()

    @tasks.loop(minutes=2)
    @Utils.time_task
    @Utils.discord_ready
    @Utils.update_tasks_list
    async def send_notifications(self) -> None:
        """Sending notifications"""
        async with self.send_notifications_lock:
            scoresaber = self.uow.bot.get_cog('ScoreSaberAPI')
            settings = self.uow.bot.get_cog("SettingsAPI")

            players = scoresaber.get_players()
            Logger.log("task", f"Sending notifications for {len(players)} players")

            for player in players:
                for guild in player.guilds:
                    score_feed_channel_id = settings.get(guild.id, "score_feed_channel_id")

                    if score_feed_channel_id is None:
                        continue

                    await self.send_notification(guild, player, score_feed_channel_id)

    async def send_notification(self, guild: Guild, player: Player, channel_id: int) -> None:
        scoresaber = self.uow.bot.get_cog('ScoreSaberAPI')

        channel = self.uow.bot.get_channel(channel_id)

        if channel is None:
            Logger.log(guild, "Recent scores channel not found, skipping!")
            return

        scores = self.get_unsent_scores(guild, player)

        Logger.log(guild, f"{player} has {len(scores)} scores to notify")

        for score in scores:
            previous_db_score = scoresaber.get_previous_score(score)

            if previous_db_score is None:
                # Post as new score
                embed = Message.get_new_score_embed(player, score, score.beatmap_version)
            else:
                # Post as improvement
                # previous_db_score = self.uow.score_repo.update_score_pp_weight(previous_db_score, self.uow.player_repo)
                embed = Message.get_improvement_score_embed(player, previous_db_score, score, score.beatmap_version)

            await channel.send(embed=embed)
            self.uow.sent_score_repo.add(SentScore(score.id, guild.id))

            # TODO: FIX LATER
            # Guild snipes leaderboard
            # if db_guild.guild_snipes:
            #     leaderboard = GuildLeaderboard(self.uow, db_guild, db_score.leaderboard_id)
            #
            #     if len(leaderboard.leaderboard_scores) > 0:
            #         guild_leaderboard_embed = Message.get_leaderboard_embed(leaderboard.get_top_scores(3))
            #         await channel.send(embed=guild_leaderboard_embed)

    def get_unsent_scores(self, guild: Guild, player: Player) -> List[Score]:
        unsent_scores = []

        for score in player.scores:
            sent_score = self.uow.sent_score_repo.get_by_score_id_and_guild_id(score.id, guild.id)

            if sent_score is None:
                unsent_scores.append(score)

        return unsent_scores
