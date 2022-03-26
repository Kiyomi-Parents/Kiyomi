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

        self.colour = Colour.random(seed=score.player.id)
        self.set_author(name=score.player.name, url=score.player.profile_url, icon_url=score.player.avatar)
        self.set_thumbnail(url=score.leaderboard.cover_image)
        self.description = F"Mapped by {score.beatmap.uploader_name} ({score.beatmap.metadata_level_author_name})"

        self.title = f"New • #{score.rank} • {score.leaderboard.song_name_full} • {score.leaderboard.difficulty_name}"

        self.add_field(name="P", value=self.pp_str)  # This should be included in the embed
        self.add_field(name="PAccuracy", value=score.accuracy)  # This should be included in the embed

        if score.modifiers is not None and len(score.modifiers) > 0:
            self.add_field(name="Modifiers", value=f"{score.modifiers}")  # This should be included in the embed

        self.add_field(name="bad_cuts", value=f"{score.bad_cuts}")  # This should be included in the embed
        self.add_field(name="missed_notes", value=f"{score.missed_notes}")  # This should be included in the embed
        self.add_field(name="max_combo", value=f"{score.max_combo}")  # This should be included in the embed

        self.add_field(name="full_combo", value=f"{score.full_combo}")  # This should be included in the embed
        # self.add_field(name="HMD", value=f"{score.mods}")  # This should be included in the embed

        self.add_field(name="Stars", value=f"{score.leaderboard.stars}")  # This should be included in the embed
        self.add_field(name="ranked", value=f"{score.leaderboard.ranked}")  # This should be included in the embed
        self.add_field(name="qualified", value=f"{score.leaderboard.qualified}")  # This should be included in the embed
        self.add_field(name="max_pp", value=f"{score.leaderboard.max_pp}")  # This should be included in the embed

        # TODO: Make buttons
        # self.add_field(name="\u200b", value=f"[Beat Saver]({score.beatmap_version.beatmap.beatsaver_url})")
        # self.add_field(name="\u200b", value=f"[Preview Map]({score.beatmap_version.beatmap.preview_url})")

    @property
    def pp_str(self) -> str:
        pp = round(self.score.pp, 2)
        pp_improvement = round(self.score.pp - self.previous_score.pp, 2)
        stock = f"**{pp}pp** +{pp_improvement}pp"

        weighted_pp_improvement = round(self.score.weighted_pp - self.previous_score.weighted_pp, 2)
        addon = f"_({self.score.weighted_pp}pp +{weighted_pp_improvement}pp)_"

        return f"{stock} {addon}"
