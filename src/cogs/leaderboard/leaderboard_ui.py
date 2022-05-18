from typing import Type

from src.cogs.leaderboard.leaderboard_cog import LeaderboardCog
from src.cogs.leaderboard.messages.components.buttons.guild_leaderboard_button import (
    GuildLeaderboardButton,
)


class LeaderboardUI(LeaderboardCog):
    @property
    def button_guild_leaderboard(self) -> Type[GuildLeaderboardButton]:
        return GuildLeaderboardButton
