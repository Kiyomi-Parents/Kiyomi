from typing import List

import pybeatsaver
from discord import Colour, Guild

from src.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from .beatsaver_embed import BeatSaverEmbed
from ....storage.model.beatmap import Beatmap
from ....storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.kiyomi import Kiyomi


class MapDetailsEmbed(BeatSaverEmbed):

    def __init__(self, bot: Kiyomi, guild: Guild, beatmap: Beatmap, beatmap_characteristic: pybeatsaver.ECharacteristic, beatmap_difficulty: pybeatsaver.EDifficulty):
        super().__init__(bot)

        self.guild = guild
        self.beatmap = beatmap

        difficulty = self.get_difficulty(beatmap_characteristic, beatmap_difficulty)

        self.title = f"{beatmap.name}"
        self.url = beatmap.beatsaver_url
        self.set_thumbnail(url=beatmap.cover_url)
        self.colour = Colour.random(seed=beatmap.uploader_id)
        self.set_author(name=beatmap.uploader_name, url=beatmap.mapper_url, icon_url=beatmap.uploader_avatar)

        self.set_footer(icon_url="https://share.lucker.xyz/qahu5/FoZozoBE67.png/raw.png", text=f"{self.get_scoresaber_status(difficulty)}")

        if beatmap.tags is not None:
            self.description = " • ".join([tag.human_readable for tag in beatmap.tags])

        self.add_field(name="Rating", value=f"{beatmap.rating}%")  # This should be included in the embed
        self.add_field(name="Length", value=f"{beatmap.length}")  # This should be included in the embed
        self.add_field(name="\u200b", value="\u200b")  # Filler for style

        # Combo these three
        self.add_field(name="NPS", value=difficulty.nps)
        self.add_field(name="BPM", value=f"{beatmap.metadata_bpm}")
        self.add_field(name="NJS", value=difficulty.njs)

        # Combo these three on a single line with icons?
        self.add_field(name="Notes", value=difficulty.notes)  # This should be included in the embed
        self.add_field(name="Bombs", value=difficulty.bombs)  # This should be included in the embed
        self.add_field(name="Obstacles", value=difficulty.obstacles)  # This should be included in the embed

        mapping_mods = self.get_mapping_mods(difficulty)
        if len(mapping_mods) > 0:
            self.add_field(name="Mapping mods", value=" • ".join(mapping_mods), inline=False)

    def get_difficulties(self) -> str:
        difficulty_texts = []

        for difficulty in self.beatmap.difficulties:
            emoji = BeatSaverUtils.difficulty_to_emoji(self.bot, self.guild, difficulty.difficulty)

            if emoji is None:
                difficulty_texts.append(difficulty.difficulty_text)
            else:
                difficulty_texts.append(str(emoji))

        return " ".join(difficulty_texts)

    def get_difficulty(self, beatmap_characteristic: pybeatsaver.ECharacteristic, beatmap_difficulty: pybeatsaver.EDifficulty) -> BeatmapVersionDifficulty:
        for difficulty in self.beatmap.difficulties:
            if difficulty.characteristic is not beatmap_characteristic:
                continue

            if difficulty.difficulty is not beatmap_difficulty:
                continue

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
