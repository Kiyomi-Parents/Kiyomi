import logging

from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands
from twitchio.ext.eventsub import StreamOnlineData, StreamOfflineData

from kiyomi.cogs.settings.storage.model.channel_setting import ChannelSetting
from .services import ServiceUnitOfWork
from .errors import BroadcastNotFound, BroadcasterNotFound, GuildTwitchBroadcasterNotFound
from .transformers.twitch_login_transformer import TwitchLoginTransformer
from kiyomi import BaseCog
from ..general import GeneralAPI

_logger = logging.getLogger(__name__)


class Twitch(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        @self.bot.events.on("twitch_broadcast_start")
        async def on_broadcast_start(event: StreamOnlineData):
            if event.type != "live":
                return

            guild_twitch_broadcasters = await self._service_uow.twitch_broadcasters.get_all_by_broadcaster_id(
                str(event.broadcaster.id))
            try:
                stream = await self._service_uow.twitch_broadcasters.fetch_stream(event.broadcaster.id)
            except BroadcastNotFound as e:
                _logger.info("Twitch", await self.bot.error_resolver.resolve_message(e, detailed=True))
                stream = None

            await self._service_uow.messages.send_broadcast_live_notifications(event, guild_twitch_broadcasters, stream)
            await self._service_uow.close()

        @self.bot.events.on("twitch_broadcast_end")
        async def on_broadcast_end(event: StreamOfflineData):
            await self._service_uow.messages.rescind_broadcast_live_notifications(event)
            await self._service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [ChannelSetting.create(self.bot, self.__cog_name__, "Twitch feed channel", "twitch_feed_channel_id")]

        self.bot.events.emit("setting_register", settings)

        await self._service_uow.events.register_subscriptions()

    twitch = app_commands.Group(name="twitch", description="Twitch commands")

    @twitch.command(name="add")
    @app_commands.describe(login="patthehyruler or https://www.twitch.tv/patthehyruler")
    async def twitch_add(self, ctx: Interaction, login: Transform[str, TwitchLoginTransformer]):
        """Link a Twitch account to yourself in this Discord guild."""
        await ctx.response.defer()

        async with self.bot.get_cog_api(GeneralAPI) as general_api:
            await general_api.register_member(ctx.guild_id, ctx.user.id)

        try:
            guild_twitch_broadcaster = await self._service_uow.twitch_broadcasters.register_twitch_broadcaster(
                ctx.guild_id, ctx.user.id, login
            )
        except BroadcasterNotFound as e:
            await ctx.followup.send(await self.bot.error_resolver.resolve_message(e))
            return

        await self._service_uow.save_changes()
        await self._service_uow.refresh(guild_twitch_broadcaster)

        await self._service_uow.events.register_subscription(
            int(guild_twitch_broadcaster.twitch_broadcaster_id)
        )  # maybe we should instead refresh all subscriptions here?

        await ctx.followup.send(
            f"Successfully linked **{guild_twitch_broadcaster.twitch_broadcaster.login}** Twitch profile!", ephemeral=True
        )

    @twitch.command(name="remove")
    async def twitch_remove(self, ctx: Interaction):
        """Remove the currently linked Twitch account from yourself in this Discord guild."""
        await ctx.response.defer()

        try:
            guild_twitch_broadcaster = await self._service_uow.twitch_broadcasters.unregister_guild_twitch_broadcaster(
                ctx.guild_id, ctx.user.id
            )
        except GuildTwitchBroadcasterNotFound:
            await ctx.followup.send(f"Failed to unregister, most likely because you are already unregistered.")
            return

        await self._service_uow.save_changes()

        await ctx.followup.send(
            f"Successfully unlinked {guild_twitch_broadcaster.twitch_broadcaster.login} from {ctx.user.name} in guild {ctx.guild.name}!",
        )

        # TODO: maybe figure out a way to delete the corresponding eventsub subscription if this streamer is orphaned?
