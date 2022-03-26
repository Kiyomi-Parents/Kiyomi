import typing
from collections import OrderedDict
from typing import Optional, List

from .leaderboard_service import LeaderboardService
from ...scoresaber.storage.model.player import Player
from ...scoresaber.storage.model.score import Score

PlayerScoreLeaderboard = Optional[typing.OrderedDict[Player, Score]]
PlayerTopScoresLeaderboard = Optional[List[Score]]


class PlayerLeaderboardService(LeaderboardService):

    async def get_player_score_leaderboard_by_guild_id_and_beatmap_key(self, guild_id: int, beatmap_key: str) -> PlayerScoreLeaderboard:
        from src.cogs.beatsaver import BeatSaverAPI
        from src.cogs.scoresaber import ScoreSaberAPI

        beatsaver = self.bot.get_cog_api(BeatSaverAPI)
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        beatmap = await beatsaver.get_beatmap_by_key(beatmap_key)

        if beatmap is None:
            return None

        leaderboard = scoresaber.get_leaderboard_by_song_hash(beatmap.latest_version.hash)

        if leaderboard is None:
            return None

        guild_players = scoresaber.get_guild_players_by_guild(guild_id)

        return self.get_player_score_leaderboard([guild_player.player for guild_player in guild_players], leaderboard.id)

    def get_player_score_leaderboard(self, players: List[Player], leaderboard_id: int) -> PlayerScoreLeaderboard:
        from src.cogs.scoresaber import ScoreSaberAPI

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

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

    def get_player_top_scores_leaderboard(self, player_id: str) -> PlayerTopScoresLeaderboard:
        from src.cogs.scoresaber import ScoreSaberAPI

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        scores = scoresaber.get_player_scores_sorted_by_pp(player_id)
        unique_scores = []

        for score in scores:
            if score.score_id not in [unique_score.score_id for unique_score in unique_scores]:
                unique_scores.append(score)

        return unique_scores
