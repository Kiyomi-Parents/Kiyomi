from typing import List

from .guild_service import GuildService
from ..storage.uow import UnitOfWork
from .channel_service import ChannelService
from .general_service import GeneralService
from ..storage.model.message import Message
from src.kiyomi import Kiyomi


class MessageService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService, channel_service: ChannelService):
        super().__init__(bot, uow)

        self.guild_service = guild_service
        self.channel_service = channel_service

    async def register_message(self, guild_id: int, channel_id: int, message_id: int) -> Message:
        message = self.uow.messages.get_by_id(message_id)

        if message is None:
            await self.guild_service.register_guild(guild_id)
            await self.channel_service.register_channel(guild_id, channel_id)

            message = self.uow.messages.add(Message(guild_id, channel_id, message_id))

            self.uow.save_changes()

        return message

    async def get_messages_in_channel(self, channel_id: int) -> List[Message]:
        return self.uow.messages.get_by_channel_id(channel_id)
