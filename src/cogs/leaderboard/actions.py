from collections import OrderedDict
from typing import Dict, Optional, List

import typing

from .storage.uow import UnitOfWork
from ..scoresaber.storage.model.player import Player
from ..scoresaber.storage.model.score import Score

PlayerScoreLeaderboard = Optional[typing.OrderedDict[Player, Score]]


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_player_score_leaderboard_by_guild_id_and_beatmap_key(self, guild_id: int, beatmap_key: str) -> PlayerScoreLeaderboard:
        beatsaver = self.uow.bot.get_cog("BeatSaverAPI")
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")

        beatmap = beatsaver.get_beatmap_by_key(beatmap_key)

        if beatmap is None:
            return None

        score = scoresaber.get_score_by_song_hash(beatmap.latest_version.hash)

        if score is None:
            return None

        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        return self.get_player_score_leaderboard([guild_player.player for guild_player in guild_players], score.leaderboard_id)

    def get_player_score_leaderboard(self, players: List[Player], leaderboard_id: int) -> PlayerScoreLeaderboard:
        scoresaber = self.uow.bot.get_cog("ScoreSaberAPI")

        leaderboard = {}

        for player in players:
            scores = scoresaber.get_score_by_player_id_and_leaderboard_id(player.id, leaderboard_id)
            best_score = self.get_best_score(scores)

            if best_score is not None:
                leaderboard[player] = best_score

        if len(leaderboard) == 0:
            return None

        return OrderedDict(sorted(leaderboard.items(), key=lambda entry: entry[1].score, reverse=True))

    @staticmethod
    def get_best_score(scores: List[Score]) -> Score:
        best_score = None

        for score in scores:
            if best_score is None:
                best_score = score
                continue

            if score.score > best_score.score:
                best_score = score

        return best_score
