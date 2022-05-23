from typing import Optional

from discord import Colour

from src.cogs.general.storage.model.guild import Guild
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi import Kiyomi
from src.kiyomi.base_embed import BaseEmbed


class ScoreEmbed(BaseEmbed):
    def __init__(self, bot: Kiyomi, guild: Guild, score: Score):
        super().__init__(bot)

        self.guild = guild
        self.score = score

        self.set_thumbnail(url=score.leaderboard.cover_image)
        self.colour = Colour.random(seed=score.player.id)

        self.set_author(
            name=f"{score.player.name} ({self.score.get_hmd_name})",
            url=score.player.profile_url,
            icon_url=score.player.avatar,
        )

        self.set_footer(
            icon_url="https://share.lucker.xyz/qahu5/FoZozoBE67.png/raw.png",
            text=self.get_scoresaber_status,
        )

        self.title = f"New • #{score.rank} • {score.leaderboard.song_name_full} • {score.leaderboard.difficulty_name}"
        self.url = score.leaderboard_url

        self.description = f"Mapped by {self.get_mapper}"

        if self.get_pp is not None:
            self.add_field(name="PP", value=self.get_pp)

        if self.get_accuracy is not None:
            self.add_field(name="Accuracy", value=self.get_accuracy)

        if self.get_modifiers is not None:
            self.add_field(name="Modifiers", value=self.get_modifiers)

        if self.get_bad_cuts is not None:
            self.add_field(name="Bad Cuts", value=self.get_bad_cuts)

        if self.get_missed_notes is not None:
            self.add_field(name="Missed Notes", value=self.get_missed_notes)

        self.add_field(name="Max Combo", value=self.get_max_combo)

    @property
    def get_max_combo(self) -> str:
        output = f"{self.score.max_combo}"

        if self.score.full_combo:
            output += f" (FC)"

        return output

    @property
    def get_pp(self) -> Optional[str]:
        if self.score.pp > 0:
            pp = round(self.score.pp, 2)
            output = f"**{pp} PP**"

            weighted_pp = self.get_weighted_pp

            if weighted_pp is None:
                return f"{output}"

            return f"{output} {weighted_pp}"

        return None

    @property
    def get_weighted_pp(self) -> Optional[str]:
        if self.score.weighted_pp > 0:
            output = f"{self.score.weighted_pp} PP"

            return f"_({output})_"

        return None

    @property
    def get_accuracy(self) -> Optional[str]:
        if self.score.accuracy is None:
            return None

        return f"{self.score.accuracy}%"

    @property
    def get_modifiers(self) -> Optional[str]:
        if self.score.modifiers is None or len(self.score.modifiers) <= 0:
            return None

        modifiers = self.score.modifiers.split(",")

        return ", ".join(modifiers)

    @property
    def get_bad_cuts(self) -> Optional[str]:
        if self.score.bad_cuts <= 0:
            return None

        return f"{self.score.bad_cuts}"

    @property
    def get_missed_notes(self) -> Optional[str]:
        if self.score.missed_notes <= 0:
            return None

        return f"{self.score.missed_notes}"

    @property
    def get_max_pp(self) -> Optional[str]:
        if self.score.leaderboard.max_pp > 0:
            return f"{self.score.leaderboard.max_pp} PP"

        return None

    @property
    def get_ranked_status(self) -> str:
        if self.score.leaderboard.ranked:
            return "Ranked"
        elif self.score.leaderboard.qualified:
            return "Qualified"

        return "Unranked"

    @property
    def get_stars(self) -> Optional[str]:
        if self.score.leaderboard.ranked or self.score.leaderboard.qualified:
            return f"{self.score.leaderboard.stars}★"

    @property
    def get_scoresaber_status(self) -> str:
        status = self.get_ranked_status

        if self.get_stars is not None:
            status += f" {self.get_stars}"

        if self.get_max_pp is not None:
            status += f" ({self.get_max_pp})"

        return status

    @property
    def get_mapper(self) -> str:
        beatmap = self.score.beatmap

        if beatmap is not None:
            return f"[{beatmap.uploader_name}]({beatmap.mapper_url}) ({beatmap.metadata_level_author_name})"

        return f"{self.score.leaderboard.level_author_name}"
