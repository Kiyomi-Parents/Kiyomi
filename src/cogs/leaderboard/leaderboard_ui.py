from typing import Type

from .services import ServiceUnitOfWork
from src.cogs.leaderboard.messages.components.buttons.guild_leaderboard_button import (
    GuildLeaderboardButton,
)
from src.kiyomi import BaseCog


class LeaderboardUI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    @property
    def button_guild_leaderboard(self) -> Type[GuildLeaderboardButton]:
        return GuildLeaderboardButton
