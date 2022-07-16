from typing import Generic, TypeVar

import discord
import pyscoresaber

from kiyomi import Kiyomi
from kiyomi.base_component import BaseComponent
from kiyomi.base_view import BaseView

T = TypeVar("T", bound=BaseView)


class LeaderboardButton(BaseComponent[T], discord.ui.Button, Generic[T]):
    def __init__(self, bot: Kiyomi, parent, beatmap_hash: str, game_mode: pyscoresaber.GameMode, difficulty: pyscoresaber.Difficulty):
        self.beatmap_hash = beatmap_hash
        self.game_mode = game_mode
        self.difficulty = difficulty

        BaseComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            label="ScoreSaber",
            style=discord.enums.ButtonStyle.primary,
            url=""
        )

    async def after_init(self):
        async with self.bot.get_cog("ScoreSaberAPI") as scoresaber_api:
            leaderboard = await scoresaber_api.get_leaderboard(self.beatmap_hash, self.game_mode, self.difficulty)

        self.url = self.leaderboard_url(leaderboard.id)

    @staticmethod
    def leaderboard_url(leaderboard_id: int) -> str:
        return f"https://scoresaber.com/leaderboard/{leaderboard_id}"
