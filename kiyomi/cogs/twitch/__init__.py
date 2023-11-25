import logging

import sentry_sdk
import twitchio
from twitchio.ext import eventsub

from .arg_resolvers.login_resolver import TwitchLoginResolver
from .arg_resolvers.user_id_resolver import TwitchUserIdResolver
from .services import ServiceUnitOfWork
from .services.event_service import EventService
from .services.twitch_broadcaster_service import TwitchBroadcasterService
from .storage import StorageUnitOfWork
from .twitch import Twitch
from kiyomi import Kiyomi, Config

_logger = logging.getLogger(__name__)


async def setup(bot: Kiyomi):
    with sentry_sdk.start_transaction(name="Twitch"):
        twitch_client = twitchio.Client.from_client_credentials(Config.get().Twitch.ClientID, Config.get().Twitch.ClientSecret, loop=bot.loop)
        eventsub_client = eventsub.EventSubClient(twitch_client, Config.get().Twitch.EventSub.WebhookSecret, Config.get().Twitch.EventSub.ListenerHost)

        bot.loop.create_task(eventsub_client.listen(port=Config.get().Twitch.EventSub.ListenerPort))

        storage_uow = StorageUnitOfWork(bot.database.session)
        service_uow = ServiceUnitOfWork(bot, storage_uow, twitch_client, eventsub_client)

        bot.error_resolver.add(TwitchLoginResolver(service_uow))
        bot.error_resolver.add(TwitchUserIdResolver(service_uow))

        await bot.add_cog(Twitch(bot, service_uow))
