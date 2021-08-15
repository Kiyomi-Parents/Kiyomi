from discord import Embed, Colour

from src.base.message_builder.score_message_builder import ScoreMessageBuilder
from src.cogs.beatsaver.storage.model import BeatmapVersion
from src.cogs.scoresaber.storage.model.player import Player
from src.cogs.scoresaber.storage.model.score import Score


class Message:

    @staticmethod
    def get_new_score_embed(player: Player, score: Score, country_rank=None):
        msg = ScoreMessageBuilder(Embed(), score, player)

        embed = msg.author().title_new(country_rank=country_rank).mapper().pp(). \
            accuracy().score_value().mods().thumbnail().url().beatmap().get_embed()

        return embed

    @staticmethod
    def get_improvement_score_embed(player: Player, previous_score: Score, score: Score, country_rank=None):
        msg = ScoreMessageBuilder(Embed(), score, player)

        embed = msg.author().title_improvement(country_rank=country_rank).mapper().pp(previous_score=previous_score). \
            accuracy(previous_score=previous_score).score_value(previous_score=previous_score). \
            mods().thumbnail().url().beatmap().get_embed()

        return embed
