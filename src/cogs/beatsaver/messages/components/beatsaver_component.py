from typing import TypeVar, Generic

from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi
from src.kiyomi.base_component import BaseComponent

T = TypeVar('T')


class BeatSaverComponent(Generic[T], BaseComponent[T]):
    def __init__(self, bot: Kiyomi, parent: T, beatmap: Beatmap):
        super().__init__(bot, parent)

        self.beatmap = beatmap
