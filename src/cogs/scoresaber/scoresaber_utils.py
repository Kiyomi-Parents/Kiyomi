import math
import re


class ScoreSaberUtils:
    @staticmethod
    def scoresaber_id_from_url(url):
        pattern = re.compile(r"(https?://scoresaber\.com/u/)?(\d{16,17})")
        match = re.match(pattern, url)

        if match:
            return match.group(2)

        return None

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
    def get_pos_from_pp_weight(weight):
        position = int(round(math.log(weight, 0.965) + 1))

        return position

    @staticmethod
    def get_pp_weight_from_pos(pos):
        pp_weight = 0.965**(pos-1)

        return pp_weight

