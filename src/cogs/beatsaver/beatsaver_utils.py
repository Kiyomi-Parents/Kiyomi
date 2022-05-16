import math
from typing import Optional

import pybeatsaver
import pyscoresaber
from discord import Emoji

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
    async def difficulty_to_emoji(
            bot: Kiyomi,
            guild_id: Optional[int],
            difficulty: pybeatsaver.EDifficulty
    ) -> Optional[Emoji]:
        setting_name = None

        if difficulty == pybeatsaver.EDifficulty.EASY:
            setting_name = "easy_difficulty_emoji"
        elif difficulty == pybeatsaver.EDifficulty.NORMAL:
            setting_name = "normal_difficulty_emoji"
        elif difficulty == pybeatsaver.EDifficulty.HARD:
            setting_name = "hard_difficulty_emoji"
        elif difficulty == pybeatsaver.EDifficulty.EXPERT:
            setting_name = "expert_difficulty_emoji"
        elif difficulty == pybeatsaver.EDifficulty.EXPERT_PLUS:
            setting_name = "expert_plus_difficulty_emoji"

        settings: "SettingsAPI" = bot.get_cog("SettingsAPI")

        return await settings.get_override_or_default(guild_id, setting_name)

    @staticmethod
    async def characteristic_to_emoji(
            bot: Kiyomi,
            guild_id: Optional[int],
            characteristic: pybeatsaver.ECharacteristic
    ) -> Optional[Emoji]:
        setting_name = None

        if characteristic == pybeatsaver.ECharacteristic.STANDARD:
            setting_name = "standard_game_mode_emoji"
        elif characteristic == pybeatsaver.ECharacteristic.ONE_SABER:
            setting_name = "one_saber_game_mode_emoji"
        elif characteristic == pybeatsaver.ECharacteristic.NO_ARROWS:
            setting_name = "no_arrows_game_mode_emoji"
        elif characteristic == pybeatsaver.ECharacteristic.DEGREE_90:
            setting_name = "90_degree_game_mode_emoji"
        elif characteristic == pybeatsaver.ECharacteristic.DEGREE_360:
            setting_name = "360_degree_game_mode_emoji"
        elif characteristic == pybeatsaver.ECharacteristic.LIGHTSHOW:
            setting_name = "lightshow_game_mode_emoji"
        elif characteristic == pybeatsaver.ECharacteristic.LAWLESS:
            setting_name = "lawless_game_mode_emoji"

        settings: "SettingsAPI" = bot.get_cog("SettingsAPI")

        return await settings.get_override_or_default(guild_id, setting_name)

    @staticmethod
    def to_scoresaber_game_mode(characteristic: pybeatsaver.ECharacteristic) -> pyscoresaber.GameMode:
        characteristics = {
            pybeatsaver.ECharacteristic.STANDARD: pyscoresaber.GameMode.STANDARD,
            pybeatsaver.ECharacteristic.ONE_SABER: pyscoresaber.GameMode.ONE_SABER,
            pybeatsaver.ECharacteristic.NO_ARROWS: pyscoresaber.GameMode.NO_ARROWS,
            pybeatsaver.ECharacteristic.DEGREE_90: pyscoresaber.GameMode.DEGREE_90,
            pybeatsaver.ECharacteristic.DEGREE_360: pyscoresaber.GameMode.DEGREE_360,
            pybeatsaver.ECharacteristic.LIGHTSHOW: pyscoresaber.GameMode.LIGHTSHOW,
            pybeatsaver.ECharacteristic.LAWLESS: pyscoresaber.GameMode.LAWLESS,
        }

        return characteristics[characteristic]

    @staticmethod
    def to_scoresaber_difficulty(difficulty: pybeatsaver.EDifficulty) -> pyscoresaber.BeatmapDifficulty:
        difficulties = {
            pybeatsaver.EDifficulty.EASY: pyscoresaber.BeatmapDifficulty.EASY,
            pybeatsaver.EDifficulty.NORMAL: pyscoresaber.BeatmapDifficulty.NORMAL,
            pybeatsaver.EDifficulty.HARD: pyscoresaber.BeatmapDifficulty.HARD,
            pybeatsaver.EDifficulty.EXPERT: pyscoresaber.BeatmapDifficulty.EXPERT,
            pybeatsaver.EDifficulty.EXPERT_PLUS: pyscoresaber.BeatmapDifficulty.EXPERT_PLUS,
        }

        return difficulties[difficulty]
