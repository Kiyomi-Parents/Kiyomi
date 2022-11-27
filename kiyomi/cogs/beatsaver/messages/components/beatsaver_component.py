from typing import TypeVar, Generic

from kiyomi.base_component import BaseComponent
from ...storage.model.beatmap import Beatmap
from kiyomi import Kiyomi

T = TypeVar("T")


class BeatSaverComponent(Generic[T], BaseComponent[T]):
    def __init__(self, bot: Kiyomi, parent: T, beatmap: Beatmap):
        super().__init__(bot, parent)

        self.beatmap = beatmap
