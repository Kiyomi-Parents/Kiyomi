from typing import TypeVar, Generic

from src.kiyomi import Kiyomi
from src.kiyomi.base_component import BaseComponent

T = TypeVar("T")


class LeaderboardComponent(Generic[T], BaseComponent[T]):
    def __init__(self, bot: Kiyomi, parent: T):
        super().__init__(bot, parent)
