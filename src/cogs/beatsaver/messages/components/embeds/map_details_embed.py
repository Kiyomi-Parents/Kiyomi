import pybeatsaver
from discord import Colour, Guild

from src.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from src.cogs.beatsaver.messages.components.embeds.beatsaver_embed import BeatSaverEmbed
from src.cogs.beatsaver.storage import Beatmap, BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailsEmbed(BeatSaverEmbed):

    def __init__(self, bot: Kiyomi, guild: Guild, beatmap: Beatmap, beatmap_difficulty: pybeatsaver.Difficulty):
        super().__init__(bot)

        self.guild = guild
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
        difficulty_texts = []

        for difficulty in self.beatmap.difficulties:
            emoji = BeatSaverUtils.difficulty_to_emoji(self.bot, self.guild, difficulty.difficulty)

            if emoji is None:
                difficulty_texts.append(difficulty.difficulty_text)
            else:
                difficulty_texts.append(str(emoji))

        return " ".join(difficulty_texts)

    def get_difficulty(self, beatmap_difficulty: pybeatsaver.Difficulty) -> BeatmapVersionDifficulty:
        for difficulty in self.beatmap.difficulties:
            if difficulty.difficulty == beatmap_difficulty:
                return difficulty
