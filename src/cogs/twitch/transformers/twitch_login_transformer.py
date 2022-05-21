import re
from typing import Union, List, Optional

from discord import Interaction
from discord.app_commands import Transformer, Choice

from ..errors import BroadcasterNotFound


class TwitchLoginTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> str:
        login = cls.twitch_login_from_url(value)

        if login is None:
            raise BroadcasterNotFound(value)

        return login

    @classmethod
    async def autocomplete(
            cls,
            interaction: Interaction,
            value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        return []  # There really shouldn't be an autocomplete for this

    @staticmethod
    def twitch_login_from_url(url: str) -> Optional[str]:
        pattern = re.compile(r"(?:https?://(?:www\.)?twitch\.tv/)?(\w+)\S*")
        match = re.match(pattern, url)

        if match:
            return match.group(1)

        return None
