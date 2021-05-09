from dateutil import tz
from datetime import datetime

import timeago
from discord import Embed, Colour


class Message:

    @staticmethod
    def get_score_embed(player, score, song):
        embed = Embed()
        embed.set_author(name=player.playerName, url=player.profile_url, icon_url=player.avatar_url)
        embed.title = f"New #{score.rank} for {score.song_name_full} on {score.difficulty_name}"
        embed.description = F"Mapped by {song._metadata['levelAuthorName']}"

        embed.add_field(name="PP", value=f"**{score.pp}pp** ({score.weighted_pp}pp)")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.playerId)
        embed.url = score.leaderboard_url

        embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
        embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")
        embed.set_footer(text=timeago.format(score.get_date, datetime.now(tz=tz.tzlocal())))

        return embed
