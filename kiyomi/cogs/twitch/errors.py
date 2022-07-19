import discord

from kiyomi.error import CogException


class TwitchCogException(CogException):
    pass


class BroadcasterNotFound(TwitchCogException):
    def __init__(self, login: str = None, user_id: int = None):
        self.twitch_login = login
        self.twitch_user_id = user_id

    def __str__(self):
        msg = f"Couldn't find Twitch Broadcaster"

        if self.twitch_login is not None:
            return f"{msg} %twitch_login%"

        if self.twitch_user_id is not None:
            return f"{msg} %twitch_user_id%"

        return f"{msg} (no more info provided)"


class BroadcastNotFound(TwitchCogException):
    def __init__(self, user_id: int):
        self.twitch_user_id = user_id

    def __str__(self):
        return f"Couldn't find Twitch Broadcast from %twitch_user_id%!"


class GuildTwitchBroadcasterNotFound(TwitchCogException):
    pass


class FailedToSendTwitchFeedMessage(TwitchCogException):
    def __init__(self, *args, original_error: Exception, channel: discord.TextChannel):
        super().__init__(*args, message_targets=[channel.guild.owner])
        self.original_error = original_error
        self.channel = channel

    def __str__(self):
        return f"Failed to send Twitch feed notification in channel (<#{self.channel.id}>)\n```{self.original_error}```"
