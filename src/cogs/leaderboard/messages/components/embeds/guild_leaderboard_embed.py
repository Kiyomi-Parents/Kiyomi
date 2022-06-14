from datetime import datetime, timezone
from typing import List

import timeago
from discord import Colour
from prettytable import PrettyTable

from src.cogs.beatsaver.storage.model.beatmap_version_difficulty import (
    BeatmapVersionDifficulty,
)
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi.base_embed import BaseEmbed
from src.kiyomi import Kiyomi


class GuildLeaderboardEmbed(BaseEmbed):
    def __init__(
        self,
        bot: Kiyomi,
        guild_name: str,
        beatmap_difficulty: BeatmapVersionDifficulty,
        leaderboard: List[Score],
    ):
        super().__init__(bot)

        self.guild_name = guild_name
        self.beatmap_difficulty = beatmap_difficulty
        self.beatmap = beatmap_difficulty.beatmap_version.beatmap
        self.leaderboard = leaderboard

        self.set_author(name=self.get_title)

        self.colour = Colour.random(seed=self.beatmap.uploader_id)

        self.title = f"{self.beatmap.name}"
        self.url = self.beatmap.beatsaver_url

        self.set_footer(
            icon_url="https://share.lucker.xyz/qahu5/FoZozoBE67.png/raw.png",
            text=self.get_scoresaber_status,
        )

        if len(leaderboard) <= 0:
            self.description = f"```Leaderboard is empty!```"
        else:
            self.description = f"```{self.get_table()}```"

    @property
    def get_title(self) -> str:
        return f"{self.guild_name} Leaderboard"

    @property
    def get_scoresaber_status(self) -> str:
        if self.beatmap_difficulty.stars is not None:
            if self.beatmap.ranked:
                return f"Ranked {self.beatmap_difficulty.stars}★"

        if self.beatmap.qualified:
            return "Qualified"

        return "Unranked"

    def get_table(self) -> str:
        table = PrettyTable()
        table.border = False
        table.field_names = ["#", "Player", "Date", "Mods", "%", "PP"]

        for index, score in enumerate(self.leaderboard):
            rank = f"#{index + 1}"
            name = score.player.name
            date = timeago.format(score.get_date, datetime.now(timezone.utc))

            if len(score.modifiers):
                mods = score.modifiers
            else:
                mods = "-"

            acc = f"{score.accuracy}%"
            pp = f"{score.pp}pp"

            table.add_row([rank, name, date, mods, acc, pp])

        return table.get_string()
