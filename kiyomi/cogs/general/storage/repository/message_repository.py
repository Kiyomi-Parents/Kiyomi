from typing import List, Type

from sqlalchemy import select

from ..model.message import Message
from kiyomi.database import BaseStorageRepository


class MessageRepository(BaseStorageRepository[Message]):
    @property
    def _table(self) -> Type[Message]:
        return Message

    async def get_all_by_channel_id(self, channel_id: int) -> List[Message]:
        stmt = select(self._table).where(self._table.channel_id == channel_id)
        result = await self._execute_scalars(stmt)
        return result.all()
