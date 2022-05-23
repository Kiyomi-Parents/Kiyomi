import os

import twitchio
from twitchio.ext import eventsub

from .arg_resolvers.login_resolver import TwitchLoginResolver
from .arg_resolvers.user_id_resolver import TwitchUserIdResolver
from .services import MessageService
from .services.event_service import EventService
from .services.twitch_broadcaster_service import BroadcasterService
from .storage import UnitOfWork
from .twitch import Twitch
from ...kiyomi import Kiyomi
from ...log import Logger


async def setup(bot: Kiyomi):
    uow = UnitOfWork(await bot.database.get_session())

    twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
    twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    twitch_access_token = os.getenv("TWITCH_ACCESS_TOKEN")
    twitch_webhook_secret = os.getenv("TWITCH_WEBHOOK_SECRET")
    twitch_event_sub_listener_url = os.getenv("TWITCH_EVENT_SUB_LISTENER_URL")
    twitch_event_sub_listener_port = os.getenv("TWITCH_EVENT_SUB_LISTENER_PORT")

    for env_var in (twitch_client_id, twitch_client_secret, twitch_event_sub_listener_url, twitch_event_sub_listener_port):
        if env_var is None or len(env_var) == 0:
            Logger.warn("Twitch", "Config issue, exiting")
            return

    twitch_client = twitchio.Client(twitch_access_token, client_secret=twitch_client_secret, loop=bot.loop)
    eventsub_client = eventsub.EventSubClient(twitch_client, twitch_webhook_secret, twitch_event_sub_listener_url)

    bot.loop.create_task(eventsub_client.listen(port=twitch_event_sub_listener_port))
    bot.loop.create_task(twitch_client.connect())

    broadcaster_service = BroadcasterService(bot, uow, twitch_client, eventsub_client)
    event_service = EventService(bot, uow, twitch_client, eventsub_client)
    message_service = MessageService(bot, uow, twitch_client, eventsub_client)

    bot.error_resolver.add(TwitchLoginResolver())
    bot.error_resolver.add(TwitchUserIdResolver(uow, broadcaster_service))

    await bot.add_cog(
        Twitch(
            bot,
            broadcaster_service,
            event_service,
            message_service
        )
    )
