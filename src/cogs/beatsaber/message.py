from datetime import datetime
from typing import List

import timeago
from dateutil import tz
from discord import Embed
from prettytable import PrettyTable

from src.cogs.beatsaber.leaderboard.leaderboard_score import LeaderboardScore
from src.cogs.beatsaber.storage.model.beatmap import Beatmap
from src.cogs.beatsaber.storage.model.player import Player
from src.cogs.beatsaber.storage.model.score import Score
from src.cogs.beatsaber.message_builder import ScoreMessageBuilder, BeatmapMessageBuilder


class Message:

    @staticmethod
    def get_score_embed(player: Player, score: Score, country_rank=None):
        msg = ScoreMessageBuilder(Embed(), score, player)

        embed = msg.author().title(country_rank=country_rank).mapper().pp().\
            accuracy().score_value().mods().thumbnail().url().beatmap().get_embed()

        return embed

    @staticmethod
    def get_new_score_embed(player: Player, score: Score, country_rank=None):
        msg = ScoreMessageBuilder(Embed(), score, player)

        embed = msg.author().title_new(country_rank=country_rank).mapper().pp().\
            accuracy().score_value().mods().thumbnail().url().beatmap().get_embed()

        return embed

    @staticmethod
    def get_improvement_score_embed(player: Player, previous_score: Score, score: Score, country_rank=None):
        msg = ScoreMessageBuilder(Embed(), score, player)

        embed = msg.author().title_improvement(country_rank=country_rank).mapper().pp(previous_score=previous_score).\
            accuracy(previous_score=previous_score).score_value(previous_score=previous_score).\
            mods().thumbnail().url().beatmap().get_embed()

        return embed

    @staticmethod
    def get_song_embed(beatmap: Beatmap):
        msg = BeatmapMessageBuilder(Embed(), beatmap)

        embed = msg.author().title().rating().downloads().\
            length().bpm().diffs().links().thumbnail().url().get_embed()

        return embed

    @staticmethod
    def get_leaderboard_embed(leaderboard_scores: List[LeaderboardScore]):
        embed = Embed()

        embed.title = "Discord Leaderboard"

        table = PrettyTable()
        table.border = False
        table.field_names = ["#", "Player", "Date", "Mods", "%", "PP"]

        for index, leaderboard_score in enumerate(leaderboard_scores):
            rank = f"#{index + 1}"
            name = leaderboard_score.db_player.player_name
            date = timeago.format(leaderboard_score.db_score.get_date, datetime.now(tz=tz.UTC))

            if len(leaderboard_score.db_score.mods):
                mods = leaderboard_score.db_score.mods
            else:
                mods = "-"

            acc = f"{leaderboard_score.db_score.accuracy}%"
            pp = f"{leaderboard_score.db_score.pp}pp"

            table.add_row([rank, name, date, mods, acc, pp])

        embed.description = f"```{table.get_string()}```"

        return embed
