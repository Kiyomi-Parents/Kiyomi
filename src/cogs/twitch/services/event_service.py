from typing import List

import twitchio
from twitchio.ext.eventsub import EventSubClient, NotificationEvent

from src.kiyomi import Kiyomi
from src.log import Logger
from .twitch_service import TwitchService
from ..storage import UnitOfWork
from ..storage.model.twitch_streamer import TwitchStreamer


class TwitchEventService(TwitchService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, twitch_client: twitchio.Client, eventsub_client: EventSubClient):
        super().__init__(bot, uow, twitch_client, eventsub_client)

        @twitch_client.event()
        async def event_eventsub_notification_stream_start(event: NotificationEvent):
            self.uow.twitch_streams.add(event.data)
            self.bot.events.emit("twitch_broadcast_start", event.data)

    async def delete_subscriptions(self):
        # ???????
        await self.register_subscription(1)
        for subscription in await self.eventsub_client.get_subscriptions():
            await self.eventsub_client.delete_subscription(subscription.id)

    async def register_subscriptions(self):
        await self.delete_subscriptions()  # ???????
        for streamer in await self.registered_streamers():
            await self.register_subscription(streamer.id)

    async def register_subscription(self, streamer_id: int):
        print(streamer_id)
        # TODO: figure out if we need to delete any previous subscriptions to the same streamer
        try:
            await self.eventsub_client.subscribe_channel_stream_start(streamer_id)
        except twitchio.errors.HTTPException as e:
            Logger.error(f"{e} stream start", e.reason)

    async def registered_streamers(self) -> List[TwitchStreamer]:
        return await self.uow.twitch_streamers.get_all()
