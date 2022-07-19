from typing import List

from .services import ServiceUnitOfWork
from .storage.model.echo_emoji import EchoEmoji
from kiyomi import BaseCog


class EmojiEchoAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def get_enabled_emojis(self, guild_id: int) -> List[EchoEmoji]:
        return await self._service_uow.echo_emojis.get_by_guild_id(guild_id)
