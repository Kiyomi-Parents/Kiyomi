from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands
from twitchio.ext.eventsub import StreamOnlineData, StreamOfflineData

from . import MessageService
from .errors import BroadcastNotFound, BroadcasterNotFound, GuildTwitchBroadcasterNotFound
from .services import BroadcasterService, EventService
from .transformers.twitch_login_transformer import TwitchLoginTransformer
from .twitch_cog import TwitchCog
from ..settings.storage import ChannelSetting
from ...kiyomi import Kiyomi


class Twitch(TwitchCog):

    def __init__(self, bot: Kiyomi, broadcaster_service: BroadcasterService,
                 event_service: EventService, message_service: MessageService):
        super().__init__(bot, broadcaster_service, event_service, message_service)
        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("twitch_broadcast_start")
        async def on_broadcast_start(event: StreamOnlineData):
            if event.type != "live":
                return

            guild_twitch_broadcasters = await self.broadcaster_service.get_all_by_broadcaster_id(str(event.broadcaster.id))
            try:
                stream = await self.broadcaster_service.fetch_stream(event.broadcaster.id)
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

        await self.event_service.register_subscriptions()

    twitch = app_commands.Group(
            name="twitch",
            description="Twitch commands"
    )

    @twitch.command(name="add")
    @app_commands.describe(login="patthehyruler or https://www.twitch.tv/patthehyruler")
    async def twitch_add(
            self,
            ctx: Interaction,
            login: Transform[str, TwitchLoginTransformer]
    ):
        """Link a Twitch account to yourself in this Discord guild."""
        self.bot.events.emit("register_member", ctx.user)

        try:
            guild_twitch_streamer = await self.broadcaster_service.register_twitch_broadcaster(ctx.guild_id, ctx.user.id, login)
        except BroadcasterNotFound as e:
            await ctx.response.send_message(await self.bot.error_resolver.resolve_message(e))
            return

        await self.event_service.register_subscription(int(guild_twitch_streamer.twitch_broadcaster_id))  # maybe we should instead refresh all subscriptions here?
        await ctx.response.send_message(f"Successfully linked **{guild_twitch_streamer.twitch_broadcaster.login}** Twitch profile!", ephemeral=True)

    @twitch.command(name="remove")
    async def twitch_remove(self, ctx: Interaction):
        """Remove the currently linked Twitch account from yourself in this Discord guild."""
        try:
            guild_twitch_broadcaster = await self.broadcaster_service.unregister_guild_twitch_broadcaster(ctx.guild_id, ctx.user.id)
        except GuildTwitchBroadcasterNotFound:
            await ctx.response.send_message(f"Failed to unregister, most likely because you are already unregistered.")
            return
        await ctx.response.send_message(f"Successfully unlinked {guild_twitch_broadcaster.twitch_broadcaster.login} from {ctx.user.name} in guild {ctx.guild.name}!", ephemeral=True)

        # TODO: maybe figure out a way to delete the corresponding eventsub subscription if this streamer is orphaned?
