from typing import Optional

from discord import Colour

from src.cogs.general.storage.model.guild import Guild
from src.cogs.score_feed.messages.components.embeds.score_feed_embed import ScoreFeedEmbed
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi import Kiyomi


class ScoreEmbed(ScoreFeedEmbed):
    def __init__(self, bot: Kiyomi, guild: Guild, score: Score, previous_score: Score):
        super().__init__(bot)

        self.guild = guild
        self.score = score
        self.previous_score = previous_score

        self.set_thumbnail(url=score.leaderboard.cover_image)
        self.colour = Colour.random(seed=score.player.id)

        self.set_author(name=f"{score.player.name} ({self.score.get_hmd_name})", url=score.player.profile_url, icon_url=score.player.avatar)
        self.set_footer(icon_url="https://share.lucker.xyz/qahu5/FoZozoBE67.png/raw.png", text=self.get_scoresaber_status)

        self.title = f"New • #{score.rank} • {score.leaderboard.song_name_full} • {score.leaderboard.difficulty_name}"
        self.url = score.leaderboard_url

        self.description = f"Mapped by {self.get_mapper}"

        if self.get_pp is not None:
            self.add_field(name="PP", value=self.get_pp)  # This should be included in the embed

        if score.accuracy is not None:
            self.add_field(name="Accuracy", value=f"{score.accuracy}%")  # This should be included in the embed

        if score.modifiers is not None and len(score.modifiers) > 0:
            self.add_field(name="Modifiers", value=f"{score.modifiers}")  # This should be included in the embed

        if score.bad_cuts > 0:
            self.add_field(name="Bad Cuts", value=f"{score.bad_cuts}")  # This should be included in the embed

        if score.missed_notes > 0:
            self.add_field(name="Missed Notes", value=f"{score.missed_notes}")  # This should be included in the embed

        self.add_field(name="Max Combo", value=self.get_max_combo)  # This should be included in the embed

        # TODO: Make buttons
        # self.add_field(name="\u200b", value=f"[Beat Saver]({score.beatmap_version.beatmap.beatsaver_url})")
        # self.add_field(name="\u200b", value=f"[Preview Map]({score.beatmap_version.beatmap.preview_url})")

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

            pp_improvement = round(self.score.pp - self.previous_score.pp, 2)

            if pp_improvement > 0:
                output += f" +{pp_improvement} PP"
            elif pp_improvement < 0:
                output += f" {pp_improvement} PP"

            return f"{output} {self.get_weighted_pp}"

        return None

    @property
    def get_weighted_pp(self) -> Optional[str]:
        if self.score.weighted_pp > 0:
            output = f"{self.score.weighted_pp} PP"

            weighted_pp_improvement = round(self.score.weighted_pp - self.previous_score.weighted_pp, 2)

            if weighted_pp_improvement > 0:
                output += f" +{weighted_pp_improvement} PP"
            elif weighted_pp_improvement < 0:
                output += f" {weighted_pp_improvement} PP"

            return f"_({output})_"

        return None

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


