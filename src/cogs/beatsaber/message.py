from datetime import datetime
from typing import List

import timeago
from dateutil import tz
from discord import Embed, Colour
from prettytable import PrettyTable

from src.cogs.beatsaber.leaderboard.leaderboard_score import LeaderboardScore


class Message:

    @staticmethod
    def get_score_embed(player, score, country_rank=None):
        song = score.song
        embed = Embed()

        embed.set_author(name=player.playerName, url=player.profile_url, icon_url=player.avatar_url)
        # TODO: maybe add a thing that also shows the score's current rank?
        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"#{score.rank} (at the time of setting) for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        else:
            embed.title = f"#{score.rank} (#{country_rank} in country) (at the time of setting) for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        
        if song is not None:
            embed.description = F"Mapped by {song.author}"

        embed.add_field(name="PP (at the time of setting)",
                        value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.playerId)
        embed.url = score.leaderboard_url

        if song is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        return embed

    @staticmethod
    def get_new_score_embed(player, score, song, country_rank=None):
        embed = Embed()
        embed.set_author(name=player.playerName, url=player.profile_url, icon_url=player.avatar_url)
        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"New #{score.rank} " \
                          f"for {score.song_name_full} on {score.difficulty_name}"
        else:
            embed.title = f"New #{score.rank} (#{country_rank} in country) " \
                          f"for {score.song_name_full} on {score.difficulty_name}"

        if song is not None:
            embed.description = F"Mapped by {song.author}"

        embed.add_field(name="PP", value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.playerId)
        embed.url = score.leaderboard_url

        if song is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        return embed

    @staticmethod
    def get_improvement_score_embed(player, previous_score, score, song, country_rank=None):
        embed = Embed()
        embed.set_author(name=player.playerName, url=player.profile_url, icon_url=player.avatar_url)
        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"Improved from #{previous_score.rank} " \
                          f"to #{score.rank} for {score.song_name_full} " \
                          f"on {score.difficulty_name}"
        else:
            embed.title = f"Improved from #{previous_score.rank} " \
                          f"to #{score.rank} (#{country_rank} in country) for {score.song_name_full} " \
                          f"on {score.difficulty_name}"

        if song is not None:
            embed.description = F"Mapped by {song.author}"

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
        embed.colour = Colour.random(seed=player.playerId)
        embed.url = score.leaderboard_url

        if song is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        return embed

    @staticmethod
    def get_song_embed(song):
        embed = Embed()

        embed.set_author(name=song.author, url=song.author_url)
        embed.title = f"{song.name}"

        embed.add_field(name="Rating", value=f"{song.rating}%")
        embed.add_field(name="Downloads", value=f"{song.downloads}")
        embed.add_field(name="Length", value=f"{song.length}")
        embed.add_field(name="BPM", value=f"{song.bpm}")

        embed.add_field(name="difficulties", value=" ".join(f"**{diff}**" for diff in song.difficulties_short))

        # Should make a simple website that redirects the user to the right links
        # discord doesn't want to make app links clickable
        # This will include OneClick links and beatmap download links
        embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        embed.set_thumbnail(url=song.cover_url)
        embed.colour = Colour.random(seed=song.author_id)
        embed.url = song.beatsaver_url

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
            name = leaderboard_score.db_player.playerName
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
