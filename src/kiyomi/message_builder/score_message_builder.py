from discord import Embed, Colour

from src.cogs.scoresaber.storage.model.player import Player
from src.cogs.scoresaber.storage.model.score import Score


class ScoreMessageBuilder:
    def __init__(self, embed: Embed,  score: Score, player: Player):
        self.embed = embed
        self.score = score
        self.player = player

        self.embed.colour = Colour.random(seed=player.id)

    def author(self):
        player = self.player
        self.embed.set_author(name=player.name, url=player.profile_url, icon_url=player.avatar)
        return self

    def title(self, country_rank=None):
        score = self.score
        if country_rank is None or not isinstance(country_rank, int):
            self.embed.title = f"#{score.rank} for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        else:
            self.embed.title = f"#{score.rank} (#{country_rank} in country) for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        return self

    def title_new(self, country_rank=None):
        score = self.score
        if country_rank is None or not isinstance(country_rank, int):
            self.embed.title = f"New #{score.rank} " \
                          f"for {score.song_name_full} on {score.difficulty_name}"
        else:
            self.embed.title = f"New #{score.rank} (#{country_rank} in country) for " \
                          f"{score.song_name_full} on {score.difficulty_name}"
        return self

    def title_improvement(self, previous_score, country_rank=None):
        score = self.score
        if country_rank is None or not isinstance(country_rank, int):
            self.embed.title = f"Improved from #{previous_score.rank} " \
                          f"to #{score.rank} for {score.song_name_full} " \
                          f"on {score.difficulty_name}"
        else:
            self.embed.title = f"Improved from #{previous_score.rank} " \
                          f"to #{score.rank} (#{country_rank} in country) for {score.song_name_full} " \
                          f"on {score.difficulty_name}"
        return self

    def mapper(self):
        score = self.score
        if score.beatmap_version is not None:
            self.embed.description = F"Mapped by {score.beatmap_version.beatmap.metadata_level_author_name}"
        return self

    def pp(self, previous_score=None):
        score = self.score
        if score.is_ranked:
            sent_improvement = False
            if previous_score is not None:
                pp_improvement = round(score.pp - previous_score.pp, 2)
                embed_string = f"**{round(score.pp, 2)}pp** +{pp_improvement}pp"
                embed_string += f"_({score.weighted_pp}pp"
                weighted_pp_improvement = round(score.weighted_pp - previous_score.weighted_pp, 2)
                embed_string += f" +{weighted_pp_improvement}pp"
                embed_string += ")_"
                self.embed.add_field(name="PP", value=embed_string)
                sent_improvement = True

            if not sent_improvement:
                self.embed.add_field(
                    name="PP",
                    value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_"
                )

        return self

    def accuracy(self, previous_score=None):
        score = self.score

        embed_string = f"**{score.accuracy}%**"
        if previous_score is not None:
            try:
                accuracy_improvement = round(score.accuracy - previous_score.accuracy, 2)
                embed_string += f" _+{accuracy_improvement}%_"
            except TypeError:
                pass

        self.embed.add_field(
            name="Accuracy",
            value=embed_string
        )
        return self

    def score_value(self, previous_score=None):
        score = self.score

        embed_string = f"{score.score}"
        if previous_score is not None:
            score_improvement = score.score - previous_score.score
            embed_string += f" _+{score_improvement}_"

        self.embed.add_field(
            name="Score",
            value=embed_string
        )
        return self

    def mods(self):
        score = self.score
        if score.mods:
            self.embed.add_field(name="Modifiers", value=f"{score.mods}")
        return self

    def thumbnail(self):
        score = self.score
        self.embed.set_thumbnail(url=score.song_image_url)
        return self

    def beatmap(self):
        score = self.score
        if score.beatmap_version is not None:
            self.embed.add_field(name="\u200b", value=f"[Beat Saver]({score.beatmap_version.beatmap.beatsaver_url})")
            self.embed.add_field(name="\u200b", value=f"[Preview Map]({score.beatmap_version.beatmap.preview_url})")
        return self

    def url(self):
        score = self.score
        self.embed.url = score.leaderboard_url
        return self

    def get_embed(self):
        return self.embed