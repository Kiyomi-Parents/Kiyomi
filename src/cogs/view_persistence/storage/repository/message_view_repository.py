from typing import Type, Optional

from sqlalchemy import select

from src.cogs.view_persistence.storage.model.message_view import MessageView
from src.kiyomi import BaseRepository


class MessageViewRepository(BaseRepository[MessageView]):
    @property
    def _table(self) -> Type[MessageView]:
        return MessageView

    async def get_by_message_id(self, message_id: int) -> Optional[MessageView]:
        stmt = select(self._table).where(self._table.message_id == message_id)
        result = await self._execute_scalars(stmt)
        return result.first()
