from discord import Embed, Colour

from src.cogs.beatsaver.storage.model import BeatmapVersion
from src.cogs.scoresaber.storage.model.player import Player
from src.cogs.scoresaber.storage.model.score import Score


class Message:

    @staticmethod
    def get_new_score_embed(player: Player, score: Score, beatmap_version: BeatmapVersion, country_rank=None):
        embed = Embed()
        embed.set_author(name=player.player_name, url=player.profile_url, icon_url=player.avatar_url)
        if country_rank is None or not isinstance(country_rank, int):
            embed.title = f"New #{score.rank} " \
                          f"for {score.song_name_full} on {score.difficulty_name}"
        else:
            embed.title = f"New #{score.rank} (#{country_rank} in country) " \
                          f"for {score.song_name_full} on {score.difficulty_name}"

        if beatmap_version is not None:
            embed.description = F"Mapped by {beatmap_version.beatmap.metadata_level_author_name}"

        embed.add_field(name="PP", value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.id)
        embed.url = score.leaderboard_url

        if beatmap_version is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({beatmap_version.beatmap.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({beatmap_version.beatmap.preview_url})")

        return embed

    @staticmethod
    def get_improvement_score_embed(player: Player, previous_score: Score, score: Score, beatmap_version: BeatmapVersion,
                                    country_rank=None):
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

        if beatmap_version is not None:
            embed.description = F"Mapped by {beatmap_version.beatmap.author}"

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
        embed.colour = Colour.random(seed=player.id)
        embed.url = score.leaderboard_url

        if beatmap_version is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({beatmap_version.beatmap.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({beatmap_version.beatmap.preview_url})")

        return embed
