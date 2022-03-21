from discord import Embed

from .storage import Player, Score
from src.kiyomi.message_builder.score_message_builder import ScoreMessageBuilder


class Message:

    @staticmethod
    def get_score_embed(player: Player, score: Score, country_rank=None):
        msg = ScoreMessageBuilder(Embed(), score, player)

        embed = msg.author().title(country_rank=country_rank).mapper().pp(). \
            accuracy().score_value().mods().thumbnail().url().beatmap().get_embed()

        return embed
