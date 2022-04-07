from typing import List

import pybeatsaver
from discord import OptionChoice

from .beatsaver_service import BeatSaverService
from ..storage import UnitOfWork
from .beatmap_service import BeatmapService
from src.kiyomi import Kiyomi
from ..storage.model.beatmap import Beatmap


class BeatmapAutocompleteService(BeatSaverService):

    def __init__(
        self,
        bot: Kiyomi,
        uow: UnitOfWork,
        beatsaver: pybeatsaver.BeatSaverAPI,
        beatmap_service: BeatmapService
    ):
        super().__init__(bot, uow, beatsaver)

        self.beatmap_service = beatmap_service

    async def get_beatmap_difficulties_by_key(self, beatmap: Beatmap, characteristic: pybeatsaver.ECharacteristic) -> List[OptionChoice]:
        beatmap_difficulties = []

        for beatmap_difficulty in beatmap.difficulties:
            if beatmap_difficulty.characteristic is not characteristic:
                continue

            beatmap_difficulties.append(
                    OptionChoice(beatmap_difficulty.difficulty_text, beatmap_difficulty.difficulty.serialize)
            )

        return beatmap_difficulties

    async def get_beatmap_characteristics_by_key(self, beatmap: Beatmap) -> List[OptionChoice]:
        beatmap_characteristics = []
        characteristics = []

        for beatmap_difficulty in beatmap.difficulties:
            if beatmap_difficulty.characteristic in characteristics:
                continue

            beatmap_characteristics.append(
                    OptionChoice(beatmap_difficulty.characteristic_text, beatmap_difficulty.characteristic.serialize)
            )
            characteristics.append(beatmap_difficulty.characteristic)

        return beatmap_characteristics
