import calendar

from twitchio import Stream
from twitchio.ext.eventsub import StreamOnlineData

from ....storage.model.guild_twitch_broadcaster import GuildTwitchBroadcaster
from src.kiyomi import Kiyomi
from .twitch_embed import TwitchEmbed


class GoLiveEmbed(TwitchEmbed):
    def __init__(self, bot: Kiyomi, event: StreamOnlineData, guild_twitch_broadcaster: GuildTwitchBroadcaster, stream: Stream):
        super().__init__(bot)

        self.set_author(
            name=f"{self.get_name(event.broadcaster.name, guild_twitch_broadcaster.member.name)} went live on Twitch!",
            icon_url=guild_twitch_broadcaster.twitch_broadcaster.profile_image_url
        )

        unix_timestamp = calendar.timegm(event.started_at.timetuple())

        self.title = stream.title
        self.url = f"https://www.twitch.tv/{guild_twitch_broadcaster.twitch_broadcaster.login}"

        self.description = f"<t:{unix_timestamp}:F>"

        self.set_image(url=stream.thumbnail_url.replace("{width}", "1920").replace("{height}", "1080"))

        self.set_footer(text=f"Playing {stream.game_name} for {stream.viewer_count} viewers!")

    @staticmethod
    def get_name(twitch_name: str, discord_name: str) -> str:
        if twitch_name.lower() == discord_name.lower():
            return twitch_name
        return f"{twitch_name} ({discord_name})"
