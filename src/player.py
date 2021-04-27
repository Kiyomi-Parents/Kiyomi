from datetime import datetime
from dateutil import tz

import timeago
from discord import Embed, Colour


class Player:

    def __init__(self, playerJson, scoresaber):
        self.playerId = playerJson["playerId"]
        self.playerName = playerJson["playerName"]
        self.avatar = playerJson["avatar"]
        self.rank = playerJson["rank"]
        self.countryRank = playerJson["countryRank"]
        self.pp = playerJson["pp"]
        self.country = playerJson["country"]
        self.role = playerJson["role"]
        self.badges = playerJson["badges"]
        self.history = playerJson["history"]
        self.permissions = playerJson["permissions"]
        self.inactive = playerJson["inactive"]
        self.banned = playerJson["banned"]

        self._scoresaber = scoresaber

    @property
    def profile_url(self):
        return f"https://scoresaber.com/u/{self.playerId}"

    @property
    def avatar_url(self):
        return f"https://new.scoresaber.com{self.avatar}"

    def get_new_scores(self):
        scores = self._scoresaber.get_recent_scores(self.playerId)
        new_scores = []

        for score in scores:
            if not score.is_saved:
                new_scores.append(score)
                score.save()

        return new_scores

    def get_score_embed(self, score, song):
        embed = Embed()
        embed.set_author(name=self.playerName, url=self.profile_url, icon_url=self.avatar_url)
        embed.title = f"New #{score.rank} for {score.song_name_full} on {score.difficulty_name}"
        embed.description = F"Mapped by {song.metadata['levelAuthorName']}"

        embed.add_field(name="PP", value=f"**{score.pp}pp** ({score.weighted_pp}pp)")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=self.playerId)
        embed.url = score.leaderboard_url

        embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
        embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")
        embed.set_footer(text=timeago.format(score.get_date(), datetime.now(tz=tz.tzlocal())))

        return embed
