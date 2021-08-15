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
    def get_pos_from_pp_weight(weight):
        position = int(round(math.log(weight, 0.965) + 1))

        return position

    @staticmethod
    def get_pp_weight_from_pos(pos):
        pp_weight = 0.965**(pos-1)

        return pp_weight

