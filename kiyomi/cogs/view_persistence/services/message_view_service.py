from __future__ import annotations

import logging
from typing import List

from kiyomi import BaseService
from ..storage import StorageUnitOfWork
from ..storage.model.message_view import MessageView
from ..storage.model.persistence import Persistence
from ..storage.repository.message_view_repository import MessageViewRepository

_logger = logging.getLogger(__name__)


class MessageViewService(BaseService[MessageView, MessageViewRepository, StorageUnitOfWork]):
    async def add_persistent_view(self, persistence: Persistence):
        async with self.bot.get_cog("GeneralAPI") as general:
            await general.register_message(persistence.guild_id, persistence.channel_id, persistence.message_id)

        await self.repository.add(MessageView(persistence.message_id, persistence.view, persistence.get_params()))

        _logger.info("View Persistence", f"Persisted view {persistence}")

    async def get_guild_channel_persistent_views(self, guild_id: int, channel_id: int) -> List[Persistence]:
        message_views = await self.repository.get_by_channel_id(channel_id)

        persistences = []
        for message_view in message_views:
            if message_view is not None:
                persistences.append(
                    Persistence(
                        guild_id,
                        channel_id,
                        message_view.message_id,
                        message_view.view_name,
                        *message_view.view_parameters,
                    )
                )

        return persistences

    async def get_guild_persistent_views(self, guild_id: int) -> List[Persistence]:
        async with self.bot.get_cog("GeneralAPI") as general:
            channels = await general.get_guild_channels(guild_id)

        persistences = []
        for channel in channels:
            persistences += await self.get_guild_channel_persistent_views(guild_id, channel.id)

        return persistences

    async def get_persistent_views(self) -> List[Persistence]:
        async with self.bot.get_cog("GeneralAPI") as general:
            guilds = await general.get_guilds()

        persistences = []
        for guild in guilds:
            guild_persistences = await self.get_guild_persistent_views(guild.id)

            _logger.info("View Persistence", f"Loaded {len(guild_persistences)} for {guild}")
            persistences += guild_persistences

        return persistences
