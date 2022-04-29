from __future__ import annotations

from typing import List, TYPE_CHECKING

from src.log import Logger
from .view_persistence_service import ViewPersistenceService
from ..storage.model.message_view import MessageView
from ..storage.model.persistence import Persistence

if TYPE_CHECKING:
    from src.cogs.general import GeneralAPI


class MessageViewService(ViewPersistenceService):

    async def add_persistent_view(self, persistence: Persistence):
        general: "GeneralAPI" = self.bot.get_cog("GeneralAPI")

        await general.register_message(persistence.guild_id, persistence.channel_id, persistence.message_id)

        self.uow.message_views.add(MessageView(persistence.message_id, persistence.view, persistence.view_parameters))

        self.uow.save_changes()

        Logger.log("View Persistence", f"Persisted view {persistence}")

    async def get_guild_channel_persistent_views(self, channel_id: int) -> List[Persistence]:
        general: "GeneralAPI" = self.bot.get_cog("GeneralAPI")

        messages = await general.get_channel_messages(channel_id)

        persistences = []
        for message in messages:
            message_view = self.uow.message_views.get_by_message_id(message.id)

            if message_view is not None:
                persistences.append(
                        Persistence(
                                message.guild_id,
                                channel_id,
                                message.id,
                                message_view.view_name,
                                *message_view.view_parameters
                        )
                )

        return persistences

    async def get_guild_persistent_views(self, guild_id: int) -> List[Persistence]:
        general: "GeneralAPI" = self.bot.get_cog("GeneralAPI")

        channels = await general.get_guild_channels(guild_id)

        persistences = []
        for channel in channels:
            persistences += await self.get_guild_channel_persistent_views(channel.id)

        return persistences

    async def get_persistent_views(self) -> List[Persistence]:
        general: "GeneralAPI" = self.bot.get_cog("GeneralAPI")

        guilds = general.get_guilds()

        persistences = []
        for guild in guilds:
            persistences += await self.get_guild_persistent_views(guild.id)

        return persistences
