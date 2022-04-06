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

    # TODO: Make smuggle sticks guild default for emojis
    @staticmethod
    async def difficulty_to_emoji(bot: Kiyomi, guild: Optional[Guild], difficulty: pybeatsaver.EDifficulty) -> Optional[Emoji]:
        if guild is None:
            return None

        settings = bot.get_cog_api(SettingsAPI)

        if difficulty == pybeatsaver.EDifficulty.EASY:
            return settings.get(guild.id, "easy_difficulty_emoji")
        elif difficulty == pybeatsaver.EDifficulty.NORMAL:
            return settings.get(guild.id, "normal_difficulty_emoji")
        elif difficulty == pybeatsaver.EDifficulty.HARD:
            return settings.get(guild.id, "hard_difficulty_emoji")
        elif difficulty == pybeatsaver.EDifficulty.EXPERT:
            return settings.get(guild.id, "expert_difficulty_emoji")
        elif difficulty == pybeatsaver.EDifficulty.EXPERT_PLUS:
            return settings.get(guild.id, "expert_plus_difficulty_emoji")

        return None

    @staticmethod
    async def characteristic_to_emoji(bot: Kiyomi, guild: Optional[Guild], characteristic: pybeatsaver.ECharacteristic) -> Optional[Emoji]:
        if guild is None:
            return None

        settings = bot.get_cog_api(SettingsAPI)

        if characteristic == pybeatsaver.ECharacteristic.STANDARD:
            return settings.get(guild.id, "standard_game_mode_emoji")
        elif characteristic == pybeatsaver.ECharacteristic.ONE_SABER:
            return settings.get(guild.id, "one_saber_game_mode_emoji")
        elif characteristic == pybeatsaver.ECharacteristic.NO_ARROWS:
            return settings.get(guild.id, "no_arrows_game_mode_emoji")
        elif characteristic == pybeatsaver.ECharacteristic.DEGREE_90:
            return settings.get(guild.id, "90_degree_game_mode_emoji")
        elif characteristic == pybeatsaver.ECharacteristic.DEGREE_360:
            return settings.get(guild.id, "360_degree_game_mode_emoji")
        elif characteristic == pybeatsaver.ECharacteristic.LIGHTSHOW:
            return settings.get(guild.id, "lightshow_game_mode_emoji")
        elif characteristic == pybeatsaver.ECharacteristic.LAWLESS:
            return settings.get(guild.id, "lawless_game_mode_emoji")

        return None
