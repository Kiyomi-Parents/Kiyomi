from typing import List

import twitchio
from twitchio.ext.eventsub import EventSubClient, NotificationEvent

from src.kiyomi import Kiyomi
from src.kiyomi.service.base_basic_service import BaseBasicService
from src.log import Logger
from ..storage import StorageUnitOfWork
from ..storage.model.twitch_broadcaster import TwitchBroadcaster


class EventService(BaseBasicService[StorageUnitOfWork]):
    def __init__(
        self, bot: Kiyomi, storage_uow: StorageUnitOfWork, twitch_client: twitchio.Client, eventsub_client: EventSubClient
    ):
        super().__init__(bot, storage_uow)

        self.eventsub_client = eventsub_client

        @twitch_client.event()
        async def event_eventsub_notification_stream_start(event: NotificationEvent):
            self.bot.events.emit("twitch_broadcast_start", event.data)

        @twitch_client.event()
        async def event_eventsub_notification_stream_end(event: NotificationEvent):
            self.bot.events.emit("twitch_broadcast_end", event.data)

    async def delete_subscriptions(self):
        # For some reason we need to first register a subscription before we can delete any subscriptions.
        await self.register_subscription(1)  # Register dummy subscription
        for subscription in await self.eventsub_client.get_subscriptions():
            await self.eventsub_client.delete_subscription(subscription.id)

    async def register_subscriptions(self):
        await self.delete_subscriptions()
        for broadcaster in await self.registered_broadcasters():
            await self.register_subscription(broadcaster.id)

    async def register_subscription(self, streamer_id: int):
        # TODO: figure out if we need to delete any previous subscriptions to the same streamer
        for subscribe in (
            self.eventsub_client.subscribe_channel_stream_start,
            self.eventsub_client.subscribe_channel_stream_end,
        ):
            try:
                await subscribe(streamer_id)
            except twitchio.errors.HTTPException as e:
                Logger.error(str(e), e.reason)

    async def registered_broadcasters(self) -> List[TwitchBroadcaster]:
        return await self.storage_uow.twitch_broadcasters.get_all()
