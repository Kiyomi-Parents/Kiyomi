import logging
from typing import List, Optional

from discord import Message, Forbidden
from twitchio import Stream
from twitchio.ext.eventsub import StreamOnlineData, StreamOfflineData

from kiyomi.cogs.settings import SettingsAPI
from kiyomi.service.base_basic_service import BaseBasicService
from ..errors import FailedToSendTwitchFeedMessage
from ..messages.components.embeds.go_live_embed import GoLiveEmbed
from ..storage import StorageUnitOfWork
from ..storage.model.guild_twitch_broadcaster import GuildTwitchBroadcaster

_logger = logging.getLogger(__name__)


class MessageService(BaseBasicService[StorageUnitOfWork]):
    async def send_broadcast_live_notifications(
        self, event: StreamOnlineData, guild_twitch_broadcasters: List[GuildTwitchBroadcaster], stream: Optional[Stream]
    ):
        if len(guild_twitch_broadcasters) == 0:
            return

        _logger.info(f"Twitch Feed", f"{event.broadcaster.name} went live, notifying {len(guild_twitch_broadcasters)} "
                                 f"guilds")

        messages = []

        for streamer in guild_twitch_broadcasters:
            try:
                message = await self.send_broadcast_live_notification(event, streamer, stream)
                messages.append(message)
            except FailedToSendTwitchFeedMessage as e:
                await e.handle(bot=self.bot)

        self.storage_uow.twitch_broadcasts.add(event, messages)

    async def send_broadcast_live_notification(
        self, event: StreamOnlineData, guild_twitch_broadcaster: GuildTwitchBroadcaster, stream: Optional[Stream]
    ) -> Optional[Message]:
        async with self.bot.get_cog_api(SettingsAPI) as settings:
            channel = await settings.get(guild_twitch_broadcaster.guild_id, "twitch_feed_channel_id")

        discord_guild = self.bot.get_guild(guild_twitch_broadcaster.guild_id)

        if channel is None:
            _logger.info(discord_guild, "Twitch feed channel not found, skipping!")
            return None

        try:
            return await channel.send(embed=GoLiveEmbed(self.bot, event, guild_twitch_broadcaster, stream))
        except Forbidden as e:
            raise FailedToSendTwitchFeedMessage(channel=channel, original_error=e)

    async def rescind_broadcast_live_notifications(self, event: StreamOfflineData):
        broadcasts = self.storage_uow.twitch_broadcasts.delete_by_broadcaster_id(event.broadcaster.id)

        _logger.info(f"Twitch Feed",
                   f"{event.broadcaster.name} went offline, updating {sum([len(broadcast.messages) for broadcast in broadcasts])} messages")

        for broadcast in broadcasts:
            for message in broadcast.messages:
                embed = message.embeds[0]
                embed.set_author(
                    name=embed.author.name + " [STREAM ENDED]", url=embed.author.url, icon_url=embed.author.icon_url
                )
                await message.edit(embed=embed)
