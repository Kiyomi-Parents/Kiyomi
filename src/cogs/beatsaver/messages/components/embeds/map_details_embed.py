from typing import List

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

        difficulty = self.get_difficulty(beatmap_difficulty)

        self.title = f"{beatmap.name}"
        self.url = beatmap.beatsaver_url
        self.set_thumbnail(url=beatmap.cover_url)
        self.colour = Colour.random(seed=beatmap.uploader_id)
        self.set_author(name=beatmap.uploader_name, url=beatmap.mapper_url, icon_url=beatmap.uploader_avatar)

        self.set_footer(icon_url="https://share.lucker.xyz/qahu5/FoZozoBE67.png/raw.png", text=f"{self.get_scoresaber_status(difficulty)}")

        self.description = f"Tag 1 • Some larger tag • this tag"  # Add tags from score saber. Needs api client support

        self.add_field(name="Rating", value=f"{beatmap.rating}%")  # This should be included in the embed
        # self.add_field(name="Length", value=f"{beatmap.length}")  # This should be included in the embed

        # VR Headset used info somewhere?

        # Combo these three
        self.add_field(name="NPS", value=difficulty.nps)
        self.add_field(name="BPM", value=f"{beatmap.metadata_bpm}")
        self.add_field(name="NJS", value=difficulty.njs)

        # Combo these three on a single line with icons?
        self.add_field(name="notes", value=difficulty.notes)  # This should be included in the embed
        self.add_field(name="bombs", value=difficulty.bombs)  # This should be included in the embed
        self.add_field(name="obstacles", value=difficulty.obstacles)  # This should be included in the embed

        mapping_mods = self.get_mapping_mods(difficulty)
        if len(mapping_mods) > 0:
            self.add_field(name="Mapping mods", value=" • ".join(mapping_mods))

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

    def get_scoresaber_status(self, difficulty: BeatmapVersionDifficulty) -> str:
        if difficulty.stars is not None:
            if self.beatmap.ranked:
                return f"Ranked {difficulty.stars}★"

        if self.beatmap.qualified:
            return "Qualified"

        return "Unranked"

    @staticmethod
    def get_mapping_mods(difficulty: BeatmapVersionDifficulty) -> List[str]:
        mods = []

        if difficulty.chroma:
            mods.append("Chroma")

        if difficulty.me:
            mods.append("Mapping Extensions")

        if difficulty.ne:
            mods.append("Noodle Extensions")

        if difficulty.cinema:
            mods.append("Cinema")

        return mods
