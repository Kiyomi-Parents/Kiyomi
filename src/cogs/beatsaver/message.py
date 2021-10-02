from discord import Embed

from src.kiyomi.message_builder.beatmap_message_builder import BeatmapMessageBuilder
from src.cogs.beatsaver.storage.model import Beatmap


class Message:

    @staticmethod
    def get_song_embed(beatmap: Beatmap):
        msg = BeatmapMessageBuilder(Embed(), beatmap)

        embed = msg.author().title().rating().downloads(). \
            length().bpm().diffs().links().thumbnail().url().get_embed()

        return embed
