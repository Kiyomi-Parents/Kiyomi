import math
from typing import Optional

import pybeatsaver
from discord import Emoji, Guild

from src.cogs.settings import SettingsAPI
from src.kiyomi import Kiyomi


class BeatSaverUtils:
    @staticmethod
    def get_max_score(blocks, max_score_per_block=115):
        max_score = 0

        if blocks >= 14:
            max_score += 8 * max_score_per_block * (blocks - 13)

        if blocks >= 6:
            max_score += 4 * max_score_per_block * (min(blocks, 13) - 5)

        if blocks >= 2:
            max_score += 2 * max_score_per_block * (min(blocks, 5) - 1)

        max_score += min(blocks, 1) * max_score_per_block

        return math.floor(max_score)

    @staticmethod
    def difficulty_to_emoji(bot: Kiyomi, guild: Optional[Guild], difficulty: pybeatsaver.Difficulty) -> Optional[Emoji]:
        if guild is None:
            return None

        settings = bot.get_cog_api(SettingsAPI)

        if difficulty == pybeatsaver.Difficulty.EASY:
            return settings.get(guild.id, "easy_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.NORMAL:
            return settings.get(guild.id, "normal_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.HARD:
            return settings.get(guild.id, "hard_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.EXPERT:
            return settings.get(guild.id, "expert_difficulty_emoji")
        elif difficulty == pybeatsaver.Difficulty.EXPERT_PLUS:
            return settings.get(guild.id, "expert_plus_difficulty_emoji")

        return None
