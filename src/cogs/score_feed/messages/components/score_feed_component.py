from typing import TypeVar, Generic

from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi import Kiyomi
from src.kiyomi.base_component import BaseComponent

T = TypeVar('T')


class ScoreFeedComponent(Generic[T], BaseComponent[T]):
    def __init__(self, bot: Kiyomi, parent: T, score: Score, previous_score: Score):
        super().__init__(bot, parent)

        self.score = score
        self.previous_score = previous_score
