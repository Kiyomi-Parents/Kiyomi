from typing import Optional, List

from discord.ext import commands

from .scoresaber_utils import ScoreSaberUtils
from .storage.model.score import Score
from .storage.uow import UnitOfWork
from .tasks import Tasks
from .actions import Actions
from .storage.model.guild_player import GuildPlayer
from .storage.model.player import Player


class ScoreSaberAPI(commands.Cog):
    def __init__(self, uow: UnitOfWork, tasks: Tasks, actions: Actions):
        self.uow = uow
        self.tasks = tasks
        self.actions = actions

    def get_guild_players_by_member_id(self, member_id: int) -> Optional[List[GuildPlayer]]:
        return self.uow.guild_player_repo.get_all_by_member_id(member_id)

    def get_player(self, player_id: str) -> Optional[Player]:
        return self.uow.player_repo.get_by_id(player_id)

    def get_players(self) -> Optional[List[Player]]:
        return self.uow.player_repo.get_all()

    def get_guild_players_by_guild(self, guild_id: int) -> Optional[List[GuildPlayer]]:
        return self.uow.guild_player_repo.get_all_by_guild_id(guild_id)

    def get_previous_score(self, score: Score) -> Optional[Score]:
        return self.uow.score_repo.get_previous_score(score)

    def get_score_by_song_hash(self, song_hash: str) -> Optional[Score]:
        return self.uow.score_repo.get_by_song_hash(song_hash)

    def get_score_by_player_id_and_leaderboard_id(self, player_id: int, leaderboard_id: int) -> Optional[List[Score]]:
        return self.uow.score_repo.get_by_player_id_and_leaderboard_id(player_id, leaderboard_id)

    def get_player_scores_sorted_by_pp(self, player_id: int) -> List[Score]:
        return self.uow.score_repo.get_player_scores_sorted_by_pp(player_id)

    def update_score_pp_weight(self, score: Score) -> Score:
        leaderboard = self.uow.bot.get_cog("LeaderboardAPI")
        top_scores_leaderboard = leaderboard.get_player_top_scores_leaderboard(score.player_id)

        position = 0

        for top_score in top_scores_leaderboard:
            if top_score.score_id == score.score_id:
                continue
            position += 1
            if top_score.pp < score.pp and position:
                break

        score.weight = ScoreSaberUtils.get_pp_weight_from_pos(position)

        return score
