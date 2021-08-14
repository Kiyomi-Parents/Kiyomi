from discord import Embed, Colour

from src.cogs.beatsaver.storage.model import Beatmap


class Message:

    @staticmethod
    def get_song_embed(beatmap: Beatmap) -> Embed:
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
