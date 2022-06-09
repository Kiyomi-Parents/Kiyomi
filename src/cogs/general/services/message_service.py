from typing import List

from ..storage.repository.message_repository import MessageRepository
from ..storage.storage_unit_of_work import StorageUnitOfWork
from ..storage.model.message import Message
from src.kiyomi import BaseService


class MessageService(BaseService[Message, MessageRepository, StorageUnitOfWork]):
    async def register_message(self, guild_id: int, channel_id: int, message_id: int) -> Message:
        if not await self.repository.exists(message_id):
            return await self.repository.add(Message(guild_id, channel_id, message_id))

    async def get_messages_in_channel(self, channel_id: int) -> List[Message]:
        return await self.repository.get_all_by_channel_id(channel_id)
