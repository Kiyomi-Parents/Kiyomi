import re
from typing import Union, List, Any, Optional

from discord import Interaction
from discord.app_commands import Transformer, Choice

from src.cogs.scoresaber.errors import PlayerNotFoundException


class ScoreSaberPlayerIdTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> str:
        player_id = cls.scoresaber_id_from_url(value)

        if player_id is None:
            raise PlayerNotFoundException(value)

        return player_id

    @classmethod
    async def autocomplete(
            cls,
            interaction: Interaction,
            value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        pass

    @staticmethod
    def scoresaber_id_from_url(url: str) -> Optional[str]:
        pattern = re.compile(r"(https?://scoresaber\.com/u/)?(\d{16,17})")
        match = re.match(pattern, url)

        if match:
            return match.group(2)

        return None
