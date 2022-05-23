from typing import Optional, List

import pyscoresaber

from src.kiyomi import Kiyomi
from .scoresaber_cog import ScoreSaberCog
from .scoresaber_utils import ScoreSaberUtils
from .services import PlayerService, ScoreService
from .storage import UnitOfWork
from .storage.model.guild_player import GuildPlayer
from .storage.model.leaderboard import Leaderboard
from .storage.model.player import Player
from .storage.model.score import Score


class ScoreSaberAPI(ScoreSaberCog):

    def __init__(self, bot: Kiyomi, player_service: PlayerService, score_service: ScoreService, uow: UnitOfWork):
        super().__init__(bot, player_service, score_service)

        self.uow = uow

    async def get_guild_players_by_member_id(self, member_id: int) -> List[GuildPlayer]:
        return await self.uow.guild_players.get_all_by_member_id(member_id)

    async def get_player(self, player_id: str) -> Optional[Player]:
        return await self.uow.players.get_by_id(player_id)

    async def get_players(self) -> List[Player]:
        return await self.uow.players.get_all()

    async def get_guild_player(self, guild_id: int, member_id: int) -> Optional[GuildPlayer]:
        return await self.uow.guild_players.get_by_guild_id_and_member_id(guild_id, member_id)

    async def get_guild_players_by_guild(self, guild_id: int) -> List[GuildPlayer]:
        return await self.uow.guild_players.get_all_by_guild_id(guild_id)

    async def get_previous_score(self, score: Score) -> Optional[Score]:
        return await self.score_service.get_previous_score(score)

    async def get_leaderboard(
            self,
            song_hash: str,
            song_game_mode: pyscoresaber.GameMode,
            song_difficulty: pyscoresaber.BeatmapDifficulty
    ) -> Optional[Leaderboard]:
        return await self.uow.leaderboards.get_by_song_hash(song_hash, song_game_mode, song_difficulty)

    async def get_score_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> List[Score]:
        return await self.uow.scores.get_all_by_player_id_and_leaderboard_id(player_id, leaderboard_id)

    async def get_player_scores_sorted_by_pp(self, player_id: str) -> List[Score]:
        return await self.uow.scores.get_all_sorted_by_pp(player_id)

    async def get_score_by_id(self, score_id: int) -> Optional[Score]:
        return await self.uow.scores.get_by_id(score_id)

    def update_score_pp_weight(self, score: Score) -> Score:
        leaderboard = self.bot.get_cog("LeaderboardAPI")
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
