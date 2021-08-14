from discord import Embed, Colour

from .storage.model.player import Player
from .storage.model.score import Score


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

        if score.beatmap_version is not None:
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
        embed.colour = Colour.random(seed=player.id)
        embed.url = score.leaderboard_url

        if score.beatmap_version is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({score.beatmap_version.beatmap.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({score.beatmap_version.beatmap.preview_url})")

        return embed
