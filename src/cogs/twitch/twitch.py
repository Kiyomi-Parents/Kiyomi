from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands
from twitchio.ext.eventsub import StreamOnlineData

from . import MessageService
from .services import TwitchStreamerService, TwitchEventService
from .transformers.twitch_login_transformer import TwitchLoginTransformer
from .twitch_cog import TwitchCog
from ..settings.storage import ChannelSetting
from ...kiyomi import Kiyomi


class Twitch(TwitchCog):

    def __init__(self, bot: Kiyomi, twitch_streamer_service: TwitchStreamerService,
                 twitch_event_service: TwitchEventService, message_service: MessageService):
        super().__init__(bot, twitch_streamer_service, twitch_event_service, message_service)
        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("twitch_broadcast_start")
        async def on_broadcast_start(event: StreamOnlineData):
            print("twitch cog received broadcast start event")
            if event.type != "live":
                print(f"Not a livestream")
                print(event)
                return

            guild_twitch_streamers = await self.twitch_streamer_service.get_guild_twitch_streamers_by_twitch_streamer_id(str(event.broadcaster.id))

            stream = await self.twitch_streamer_service.get_stream(event.broadcaster.id)

            await self.message_service.send_broadcast_live_notifications(event, guild_twitch_streamers, stream)

    @commands.Cog.listener()
    async def on_ready(self):
        print("twitch cog on_ready")
        settings = [
            ChannelSetting.create(self.bot, "Twitch feed channel", "twitch_feed_channel_id")
        ]

        self.bot.events.emit("setting_register", settings)

        await self.twitch_event_service.register_subscriptions()

    twitch = app_commands.Group(
            name="twitch",
            description="Twitch commands"
    )

    @twitch.command(name="test")
    @app_commands.describe(arg="what")
    async def twitch_test(
            self,
            ctx: Interaction,
            arg: str
    ):
        user = await self.twitch_streamer_service.get_user(arg)
        print(user)

    @twitch.command(name="add")
    @app_commands.describe(login="patthehyruler")
    async def twitch_add(
            self,
            ctx: Interaction,
            login: Transform[str, TwitchLoginTransformer]
    ):
        self.bot.events.emit("register_member", ctx.user)
        guild_twitch_streamer = await self.twitch_streamer_service.register_twitch_streamer(ctx.guild_id, ctx.user.id, login)
        await self.twitch_event_service.register_subscription(int(guild_twitch_streamer.twitch_streamer_id))  # maybe we should instead refresh all subscriptions here?

    async def twitch_remove(self):
        pass
