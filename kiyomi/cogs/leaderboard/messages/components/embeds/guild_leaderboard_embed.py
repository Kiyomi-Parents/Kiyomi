from datetime import datetime, timezone

import timeago
from discord import Colour
from prettytable import PrettyTable

from ....storage.models.guild_leaderboard import GuildLeaderboard
from kiyomi.base_embed import BaseEmbed
from kiyomi import Kiyomi


class GuildLeaderboardEmbed(BaseEmbed):
    def __init__(
        self,
        bot: Kiyomi,
        guild_name: str,
        guild_leaderboard: GuildLeaderboard,
    ):
        super().__init__(bot)

        self.guild_name = guild_name
        self.guild_leaderboard = guild_leaderboard

        self.set_author(name=self.get_title)

        self.colour = Colour.random(seed=self.guild_leaderboard.leaderboard.id)

        self.title = f"{self.guild_leaderboard.leaderboard.song_name_full}"
        self.url = self.guild_leaderboard.leaderboard.leaderboard_url

        self.set_footer(
            icon_url="https://share.lucker.xyz/qahu5/FoZozoBE67.png/raw.png",
            text=self.get_scoresaber_status,
        )

        if len(self.guild_leaderboard.scores) <= 0:
            self.description = f"```Leaderboard is empty!```"
        else:
            self.description = f"```{self.get_table()}```"

    @property
    def get_title(self) -> str:
        return f"{self.guild_name} Leaderboard"

    @property
    def get_scoresaber_status(self) -> str:
        if self.guild_leaderboard.leaderboard.ranked:
            return f"Ranked {self.guild_leaderboard.leaderboard.stars}★"

        if self.guild_leaderboard.leaderboard.qualified:
            return "Qualified"

        return "Unranked"

    def get_table(self) -> str:
        table = PrettyTable()
        table.border = False
        table.field_names = ["#", "Player", "Date", "Mods", "%", "PP"]

        for index, score in enumerate(self.guild_leaderboard.scores):
            rank = f"#{index + 1}"
            name = score.player.name_truncated
            date = timeago.format(score.get_date, datetime.now(timezone.utc))

            if len(score.modifiers):
                mods = score.modifiers
            else:
                mods = "-"

            if score.accuracy is None:
                acc = f"???"
            else:
                acc = f"{score.accuracy}%"

            pp = f"{score.pp}pp"

            table.add_row([rank, name, date, mods, acc, pp])

        return table.get_string()
