from src.kiyomi.error import CogException


class TwitchCogException(CogException):
    pass


class BroadcasterNotFound(TwitchCogException):
    def __init__(self, login: str):
        self.twitch_login = login

    def __str__(self):
        return f"Couldn't find Twitch Broadcaster with login %twitch_login%!"


class BroadcastNotFound(TwitchCogException):
    def __init__(self, user_id: int):
        self.twitch_user_id = user_id

    def __str__(self):
        return f"Couldn't find Twitch Broadcast from user id %twitch_user_id%!"


class GuildTwitchBroadcasterNotFound(TwitchCogException):
    pass
