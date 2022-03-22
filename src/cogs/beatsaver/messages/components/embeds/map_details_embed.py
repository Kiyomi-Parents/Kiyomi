import pybeatsaver
from discord import Colour

from src.cogs.beatsaver.messages.components.embeds.embed import BeatSaverEmbed
from src.cogs.beatsaver.storage import Beatmap, BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailsEmbed(BeatSaverEmbed):

    def __init__(self, bot: Kiyomi, beatmap: Beatmap, beatmap_difficulty: pybeatsaver.Difficulty):
        super().__init__(bot)

        self.beatmap = beatmap

        self.title = f"{beatmap.name}"
        self.url = beatmap.beatsaver_url
        self.set_thumbnail(url=beatmap.cover_url)
        self.colour = Colour.random(seed=beatmap.uploader_id)
        self.set_author(name=beatmap.uploader_name, url=beatmap.mapper_url, icon_url=beatmap.uploader_avatar)

        self.add_field(name="Rating", value=f"{beatmap.rating}%")
        self.add_field(name="Downloads", value=f"{beatmap.stats_downloads}")
        self.add_field(name="Length", value=f"{beatmap.length}")
        self.add_field(name="BPM", value=f"{beatmap.metadata_bpm}")
        self.add_field(name="Difficulties", value=self.get_difficulties())
        self.add_field(name="difficulty", value=self.get_difficulty(beatmap_difficulty).difficulty)

    def get_difficulties(self) -> str:
        return " ".join(f"**{diff.difficulty_text}**" for diff in self.beatmap.difficulties)

    def get_difficulty(self, beatmap_difficulty: pybeatsaver.Difficulty) -> BeatmapVersionDifficulty:
        print(self.beatmap.difficulties)
        for difficulty in self.beatmap.difficulties:
            if difficulty.difficulty == beatmap_difficulty:
                return difficulty
