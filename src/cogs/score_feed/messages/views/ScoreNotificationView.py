from typing import Optional

from discord import Guild

from src.cogs.score_feed.messages.components.buttons.beatsaver_button import BeatSaverButton
from src.cogs.score_feed.messages.components.buttons.score_button import ScoreButton
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi import Kiyomi
from src.kiyomi.base_view import BaseView


class ScoreNotificationView(BaseView):
    def __init__(self, bot: Kiyomi, guild: Guild, score: Score, previous_score: Optional[Score]):
        self.score = score
        self.previous_score = previous_score

        super().__init__(bot, guild)

    def update_buttons(self):
        self.add_item(ScoreButton(self.bot, self, self.score, self.previous_score))

        if self.score.beatmap is not None:
            self.add_item(BeatSaverButton(self.bot, self, self.score.beatmap.id))
