from typing import List

from twitchio import Stream
from twitchio.ext.eventsub import StreamOnlineData

from src.cogs.settings import SettingsAPI
from src.log import Logger
from ..messages.components.embeds.go_live_embed import GoLiveEmbed
from ..services import TwitchService
from ..storage.model.guild_twitch_streamer import GuildTwitchStreamer


class MessageService(TwitchService):
    async def send_broadcast_live_notifications(self, event: StreamOnlineData, guild_twitch_streamers: List[GuildTwitchStreamer], stream: Stream):
        if len(guild_twitch_streamers) == 0:
            print("adfasfds")
            return

        Logger.log(f"Twitch Feed", f"{event.broadcaster.name} went live, notifying {len(guild_twitch_streamers)} guilds")

        for streamer in guild_twitch_streamers:
            await self.send_broadcast_live_notification(event, streamer, stream)

    async def send_broadcast_live_notification(self, event: StreamOnlineData, guild_twitch_streamer: GuildTwitchStreamer, stream: Stream):
        settings = self.bot.get_cog_api(SettingsAPI)

        discord_guild = self.bot.get_guild(guild_twitch_streamer.guild_id)

        channel = await settings.get(guild_twitch_streamer.guild_id, "twitch_feed_channel_id")

        if channel is None:
            Logger.log(discord_guild, "Twitch feed channel not found, skipping!")
            return

        await channel.send(embed=GoLiveEmbed(self.bot, event, guild_twitch_streamer, stream))
