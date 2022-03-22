from datetime import datetime
from typing import Optional

import timeago
from dateutil import tz
from discord import Embed
from prettytable import PrettyTable

from src.cogs.leaderboard.messages.components.embeds.embed import LeaderboardEmbed
from src.cogs.leaderboard.services import PlayerScoreLeaderboard
from src.kiyomi import Kiyomi


# TODO: handle multiple difficulties somehow

class GuildLeaderboardEmbed(LeaderboardEmbed):
    def __init__(self, bot: Kiyomi, beatmap_id: str):
        super().__init__(bot)

        self.beatmap_id = beatmap_id

    async def get_embed(self, leaderboard: Optional[PlayerScoreLeaderboard]) -> Embed:
        embed = Embed()

        embed.title = "Discord Leaderboard"

        if leaderboard is None:
            embed.description = f"```Leaderboard is empty!```"

            return embed

        table = PrettyTable()
        table.border = False
        table.field_names = ["#", "Player", "Date", "Mods", "%", "PP"]

        for index, (player, score) in enumerate(leaderboard.items()):
            rank = f"#{index + 1}"
            name = player.player_name
            date = timeago.format(score.get_date, datetime.now(tz=tz.UTC))

            if len(score.mods):
                mods = score.mods
            else:
                mods = "-"

            acc = f"{score.accuracy}%"
            pp = f"{score.pp}pp"

            table.add_row([rank, name, date, mods, acc, pp])

        embed.description = f"```{table.get_string()}```"

        return embed
