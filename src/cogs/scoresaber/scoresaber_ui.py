from typing import Type

from src.cogs.scoresaber.messages.components.buttons.score_button import ScoreButton
from src.cogs.scoresaber.messages.views.score_view import ScoreView
from src.cogs.scoresaber.scoresaber_cog import ScoreSaberCog


class ScoreSaberUI(ScoreSaberCog):
    @property
    def button_score(self) -> Type[ScoreButton]:
        return ScoreButton

    @property
    def view_score(self) -> Type[ScoreView]:
        return ScoreView
