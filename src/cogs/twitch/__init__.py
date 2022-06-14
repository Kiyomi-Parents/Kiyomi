import os

import twitchio
from twitchio.ext import eventsub

from .arg_resolvers.login_resolver import TwitchLoginResolver
from .arg_resolvers.user_id_resolver import TwitchUserIdResolver
from .services import ServiceUnitOfWork
from .services.event_service import EventService
from .services.twitch_broadcaster_service import TwitchBroadcasterService
from .storage import StorageUnitOfWork
from .twitch import Twitch
from src.kiyomi import Kiyomi
from src.log import Logger


async def setup(bot: Kiyomi):
    twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
    twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    twitch_webhook_secret = os.getenv("TWITCH_WEBHOOK_SECRET")
    twitch_event_sub_listener_url = os.getenv("TWITCH_EVENT_SUB_LISTENER_URL")
    twitch_event_sub_listener_port = os.getenv("TWITCH_EVENT_SUB_LISTENER_PORT")

    for env_var in (twitch_client_id, twitch_client_secret, twitch_event_sub_listener_url, twitch_event_sub_listener_port):
        if env_var is None or len(env_var) == 0:
            Logger.warn("Twitch", "Config issue, exiting")
            return

    twitch_client = twitchio.Client.from_client_credentials(twitch_client_id, twitch_client_secret, loop=bot.loop)
    eventsub_client = eventsub.EventSubClient(twitch_client, twitch_webhook_secret, twitch_event_sub_listener_url)

    async def connect():
        try:
            await twitch_client.connect()
        except twitchio.errors.AuthenticationError as e:
            Logger.error("Twitch", f"{e.__class__.__name__}: {e}")

    bot.loop.create_task(eventsub_client.listen(port=twitch_event_sub_listener_port))
    bot.loop.create_task(connect())

    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow, twitch_client, eventsub_client)

    bot.error_resolver.add(TwitchLoginResolver(service_uow))
    bot.error_resolver.add(TwitchUserIdResolver(service_uow))

    await bot.add_cog(Twitch(bot, service_uow))
