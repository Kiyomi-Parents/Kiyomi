from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi
from src.kiyomi.base_component import BaseComponent


class BeatSaverComponent(BaseComponent):
    def __init__(self, bot: Kiyomi, events: AsyncIOEventEmitter, beatmap: Beatmap):
        super().__init__(bot, events)

        self.beatmap = beatmap
