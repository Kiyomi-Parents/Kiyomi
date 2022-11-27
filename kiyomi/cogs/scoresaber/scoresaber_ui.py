from typing import Type

from .messages.components.buttons.leaderboard_button import LeaderboardButton
from .services import ServiceUnitOfWork
from .messages.components.buttons.score_button import ScoreButton
from .messages.views.score_view import ScoreView
from kiyomi import BaseCog


class ScoreSaberUI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    @property
    def button_score(self) -> Type[ScoreButton]:
        return ScoreButton

    @property
    def button_leaderboard(self) -> Type[LeaderboardButton]:
        return LeaderboardButton

    @property
    def view_score(self) -> Type[ScoreView]:
        return ScoreView
