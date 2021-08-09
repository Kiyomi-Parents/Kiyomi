from datetime import datetime
from typing import List

import timeago
from dateutil import tz
from discord import Embed, Colour
from prettytable import PrettyTable

from src.cogs.beatsaber.leaderboard.leaderboard_score import LeaderboardScore
from src.cogs.beatsaber.storage.model.beatmap import Beatmap
from src.cogs.beatsaber.storage.model.player import Player
from src.cogs.beatsaber.storage.model.score import Score


class Message:

    @staticmethod
    def get_score_embed(player: Player, score: Score, country_rank=None):
        embed = Embed()

        embed.set_author(name=player.player_name, url=player.profile_url, icon_url=player.avatar_url)

        # TODO: maybe add a thing that also shows the score's current rank?
        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"#{score.rank} (at the time of setting) for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        else:
            embed.title = f"#{score.rank} (#{country_rank} in country) (at the time of setting) for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        
        if score.beatmap_version.beatmap is not None:
            embed.description = F"Mapped by {score.beatmap_version.beatmap.metadata_level_author_name}"

        embed.add_field(
            name="PP (at the time of setting)",
            value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_"
        )
        embed.add_field(
            name="Accuracy",
            value=f"**{score.accuracy}%**"
        )
        embed.add_field(
            name="Score",
            value=f"{score.score}"
        )

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.player_id)
        embed.url = score.leaderboard_url

        if score.beatmap_version.beatmap is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({score.beatmap_version.beatmap.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({score.beatmap_version.beatmap.preview_url})")

        return embed

    @staticmethod
    def get_new_score_embed(player: Player, score: Score, beatmap: Beatmap, country_rank=None):
        embed = Embed()
        embed.set_author(name=player.player_name, url=player.profile_url, icon_url=player.avatar_url)
        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"New #{score.rank} " \
                          f"for {score.song_name_full} on {score.difficulty_name}"
        else:
            embed.title = f"New #{score.rank} (#{country_rank} in country) " \
                          f"for {score.song_name_full} on {score.difficulty_name}"

        if beatmap is not None:
            embed.description = F"Mapped by {beatmap.metadata_level_author_name}"

        embed.add_field(name="PP", value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.player_id)
        embed.url = score.leaderboard_url

        if beatmap is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({beatmap.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({beatmap.preview_url})")

        return embed

    @staticmethod
    def get_improvement_score_embed(player: Player, previous_score: Score, score: Score, beatmap: Beatmap, country_rank=None):
        embed = Embed()
        embed.set_author(name=player.player_name, url=player.profile_url, icon_url=player.avatar_url)

        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"Improved from #{previous_score.rank} " \
                          f"to #{score.rank} for {score.song_name_full} " \
                          f"on {score.difficulty_name}"
        else:
            embed.title = f"Improved from #{previous_score.rank} " \
                          f"to #{score.rank} (#{country_rank} in country) for {score.song_name_full} " \
                          f"on {score.difficulty_name}"

        if beatmap is not None:
            embed.description = F"Mapped by {beatmap.author}"

        pp_improvement = round(score.pp - previous_score.pp, 2)
        weighted_pp_improvement = round(score.weighted_pp - previous_score.weighted_pp, 2)

        embed.add_field(name="PP", value=f"**{round(score.pp, 2)}pp** +{pp_improvement}pp\n"
                                         f"_({score.weighted_pp}pp +{weighted_pp_improvement}pp)_")

        try:
            accuracy_improvement = round(score.accuracy - previous_score.accuracy, 2)
            embed.add_field(name="Accuracy", value=f"**{score.accuracy}%** _+{accuracy_improvement}%_")
        except TypeError:
            pass

        score_improvement = score.score - previous_score.score
        embed.add_field(name="Score", value=f"{score.score} _+{score_improvement}_")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.player_id)
        embed.url = score.leaderboard_url

        if beatmap is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({beatmap.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({beatmap.preview_url})")

        return embed

    @staticmethod
    def get_song_embed(beatmap: Beatmap):
        embed = Embed()

        embed.set_author(name=beatmap.uploader_name, url=beatmap.mapper_url, icon_url=beatmap.uploader_avatar)
        embed.title = f"{beatmap.name}"

        embed.add_field(name="Rating", value=f"{beatmap.rating}%")
        embed.add_field(name="Downloads", value=f"{beatmap.stats_downloads}")
        embed.add_field(name="Length", value=f"{beatmap.length}")
        embed.add_field(name="BPM", value=f"{beatmap.metadata_bpm}")

        embed.add_field(name="difficulties", value=" ".join(f"**{diff}**" for diff in beatmap.difficulties_short))

        # Should make a simple website that redirects the user to the right links
        # discord doesn't want to make app links clickable
        # This will include OneClick links and beatmap download links
        embed.add_field(name="\u200b", value=f"[Preview Map]({beatmap.preview_url})")

        embed.set_thumbnail(url=beatmap.cover_url)
        embed.colour = Colour.random(seed=beatmap.uploader_id)
        embed.url = beatmap.beatsaver_url

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
