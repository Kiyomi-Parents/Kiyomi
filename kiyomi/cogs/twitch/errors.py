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
