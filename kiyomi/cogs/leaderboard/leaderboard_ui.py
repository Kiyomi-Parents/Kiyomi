from typing import Type

from kiyomi.cogs.leaderboard.messages.components.buttons.guild_leaderboard_button import (
    GuildLeaderboardButton,
)
from .services import ServiceUnitOfWork
from kiyomi import BaseCog


class LeaderboardUI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    @property
    def button_guild_leaderboard(self) -> Type[GuildLeaderboardButton]:
        return GuildLeaderboardButton
