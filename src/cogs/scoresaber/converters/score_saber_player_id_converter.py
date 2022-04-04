import re
from typing import Optional

from discord.ext.commands import Context

from src.cogs.scoresaber.errors import PlayerNotFoundException
from src.kiyomi.base_converter import BaseConverter


class ScoreSaberPlayerIdConverter(BaseConverter):

    async def convert(self, ctx: Context, argument: str) -> str:
        player_id = self.scoresaber_id_from_url(argument)

        if player_id is None:
            raise PlayerNotFoundException(argument)

        return player_id

    @staticmethod
    def scoresaber_id_from_url(url: str) -> Optional[str]:
        pattern = re.compile(r"(https?://scoresaber\.com/u/)?(\d{16,17})")
        match = re.match(pattern, url)

        if match:
            return match.group(2)

        return None
