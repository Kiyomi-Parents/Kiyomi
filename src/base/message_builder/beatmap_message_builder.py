from discord import Embed, Colour


class BeatmapMessageBuilder:
    def __init__(self, embed: Embed, beatmap):
        self.embed = embed
        self.beatmap = beatmap

        self.embed.colour = Colour.random(seed=beatmap.uploader_id)

    def author(self):
        beatmap = self.beatmap
        self.embed.set_author(name=beatmap.uploader_name, url=beatmap.mapper_url, icon_url=beatmap.uploader_avatar)
        return self

    def title(self):
        beatmap = self.beatmap
        self.embed.title = f"{beatmap.name}"
        return self

    def rating(self):
        beatmap = self.beatmap
        self.embed.add_field(name="Rating", value=f"{beatmap.rating}%")
        return self

    def downloads(self):
        beatmap = self.beatmap
        self.embed.add_field(name="Downloads", value=f"{beatmap.stats_downloads}")
        return self

    def length(self):
        beatmap = self.beatmap
        self.embed.add_field(name="Length", value=f"{beatmap.length}")
        return self

    def bpm(self):
        beatmap = self.beatmap
        self.embed.add_field(name="BPM", value=f"{beatmap.metadata_bpm}")
        return self

    def diffs(self):
        beatmap = self.beatmap
        self.embed.add_field(name="difficulties", value=" ".join(f"**{diff}**" for diff in beatmap.difficulties_short))
        return self

    def links(self):
        beatmap = self.beatmap
        # TODO: Should make a simple website that redirects the user to the right links
        # discord doesn't want to make app links clickable
        # This will include OneClick links and beatmap download links
        self.embed.add_field(name="\u200b", value=f"[Preview Map]({beatmap.preview_url})")
        return self

    def thumbnail(self):
        beatmap = self.beatmap
        self.embed.set_thumbnail(url=beatmap.cover_url)
        return self

    def url(self):
        beatmap = self.beatmap
        self.embed.url = beatmap.beatsaver_url
        return self

    def get_embed(self):
        return self.embed
