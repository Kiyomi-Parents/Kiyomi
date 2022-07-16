from typing import TypeVar, Generic

from kiyomi.base_component import BaseComponent
from kiyomi import Kiyomi

T = TypeVar("T")


class LeaderboardComponent(Generic[T], BaseComponent[T]):
    def __init__(self, bot: Kiyomi, parent: T):
        super().__init__(bot, parent)
