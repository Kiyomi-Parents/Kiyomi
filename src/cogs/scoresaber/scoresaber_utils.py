import math

import pybeatsaver
import pyscoresaber


class ScoreSaberUtils:
    @staticmethod
    def get_pos_from_pp_weight(weight):
        position = int(round(math.log(weight, 0.965) + 1))

        return position

    @staticmethod
    def get_pp_weight_from_pos(pos):
        pp_weight = 0.965 ** (pos - 1)

        return pp_weight

    @staticmethod
    def to_beatsaver_characteristic(
        game_mode: pyscoresaber.GameMode,
    ) -> pybeatsaver.ECharacteristic:
        game_modes = {
            pyscoresaber.GameMode.STANDARD: pybeatsaver.ECharacteristic.STANDARD,
            pyscoresaber.GameMode.ONE_SABER: pybeatsaver.ECharacteristic.ONE_SABER,
            pyscoresaber.GameMode.NO_ARROWS: pybeatsaver.ECharacteristic.NO_ARROWS,
            pyscoresaber.GameMode.DEGREE_90: pybeatsaver.ECharacteristic.DEGREE_90,
            pyscoresaber.GameMode.DEGREE_360: pybeatsaver.ECharacteristic.DEGREE_360,
            pyscoresaber.GameMode.LIGHTSHOW: pybeatsaver.ECharacteristic.LIGHTSHOW,
            pyscoresaber.GameMode.LAWLESS: pybeatsaver.ECharacteristic.LAWLESS,
        }

        return game_modes[game_mode]

    @staticmethod
    def to_beatsaver_difficulty(
        difficulty: pyscoresaber.BeatmapDifficulty,
    ) -> pybeatsaver.EDifficulty:
        difficulties = {
            pyscoresaber.BeatmapDifficulty.EASY: pybeatsaver.EDifficulty.EASY,
            pyscoresaber.BeatmapDifficulty.NORMAL: pybeatsaver.EDifficulty.NORMAL,
            pyscoresaber.BeatmapDifficulty.HARD: pybeatsaver.EDifficulty.HARD,
            pyscoresaber.BeatmapDifficulty.EXPERT: pybeatsaver.EDifficulty.EXPERT,
            pyscoresaber.BeatmapDifficulty.EXPERT_PLUS: pybeatsaver.EDifficulty.EXPERT_PLUS,
        }

        return difficulties[difficulty]
