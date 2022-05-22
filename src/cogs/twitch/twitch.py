from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands
from twitchio.ext.eventsub import StreamOnlineData, StreamOfflineData

from . import MessageService
from .errors import BroadcastNotFound
from .services import BroadcasterService, EventService
from .transformers.twitch_login_transformer import TwitchLoginTransformer
from .twitch_cog import TwitchCog
from ..settings.storage import ChannelSetting
from ...kiyomi import Kiyomi


class Twitch(TwitchCog):

    def __init__(self, bot: Kiyomi, twitch_broadcaster_service: BroadcasterService,
                 twitch_event_service: EventService, message_service: MessageService):
        super().__init__(bot, twitch_broadcaster_service, twitch_event_service, message_service)
        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("twitch_broadcast_start")
        async def on_broadcast_start(event: StreamOnlineData):
            if event.type != "live":
                return

            guild_twitch_broadcasters = await self.twitch_broadcaster_service.get_guild_twitch_broadcasters_by_broadcaster_id(str(event.broadcaster.id))
            try:
                stream = await self.twitch_broadcaster_service.fetch_stream(event.broadcaster.id)
            except BroadcastNotFound:
                stream = None

            await self.message_service.send_broadcast_live_notifications(event, guild_twitch_broadcasters, stream)

        @self.bot.events.on("twitch_broadcast_end")
        async def on_broadcast_end(event: StreamOfflineData):
            await self.message_service.rescind_broadcast_live_notifications(event)

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ChannelSetting.create(self.bot, "Twitch feed channel", "twitch_feed_channel_id")
        ]

        self.bot.events.emit("setting_register", settings)

        await self.twitch_event_service.register_subscriptions()

    twitch = app_commands.Group(
            name="twitch",
            description="Twitch commands"
    )

    @twitch.command(name="add")
    @app_commands.describe(login="patthehyruler")
    async def twitch_add(
            self,
            ctx: Interaction,
            login: Transform[str, TwitchLoginTransformer]
    ):
        self.bot.events.emit("register_member", ctx.user)
        guild_twitch_streamer = await self.twitch_broadcaster_service.register_twitch_broadcaster(ctx.guild_id, ctx.user.id, login)
        await self.twitch_event_service.register_subscription(int(guild_twitch_streamer.twitch_broadcaster_id))  # maybe we should instead refresh all subscriptions here?

    @twitch.command(name="remove")
    async def twitch_remove(self, ctx: Interaction):
        pass
