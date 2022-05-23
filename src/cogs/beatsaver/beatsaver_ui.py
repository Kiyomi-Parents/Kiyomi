from typing import Type

from src.cogs.beatsaver.beatsaver_cog import BeatSaverCog
from src.cogs.beatsaver.messages.components.buttons.beatsaver_button import (
    BeatSaverButton,
)
from src.cogs.beatsaver.messages.components.buttons.map_details_button import (
    MapDetailsButton,
)
from src.cogs.beatsaver.messages.components.buttons.map_preview_button import (
    MapPreviewButton,
)
from src.cogs.beatsaver.messages.components.selects.map_detail_characteristic_select import (
    MapDetailCharacteristicSelect,
)
from src.cogs.beatsaver.messages.components.selects.map_detail_difficulty_select import (
    MapDetailDifficultySelect,
)


class BeatSaverUI(BeatSaverCog):
    @property
    def select_map_detail_characteristic(self) -> Type[MapDetailCharacteristicSelect]:
        return MapDetailCharacteristicSelect

    @property
    def select_map_detail_difficulty(self) -> Type[MapDetailDifficultySelect]:
        return MapDetailDifficultySelect

    @property
    def button_beat_saver(self) -> Type[BeatSaverButton]:
        return BeatSaverButton

    @property
    def button_map_details(self) -> Type[MapDetailsButton]:
        return MapDetailsButton

    @property
    def button_map_preview(self) -> Type[MapPreviewButton]:
        return MapPreviewButton
