from src.kiyomi.error import CogException


class TwitchCogException(CogException):
    pass


class BroadcasterNotFound(TwitchCogException):
    def __init__(self, login: str):
        self.login = login

    def __str__(self):
        # TODO: fancy arg resolver
        return f"Couldn't find Twitch Broadcaster with login {self.login}!"


class BroadcastNotFound(TwitchCogException):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        # TODO: fancy arg resolver
        return f"Couldn't find Twitch Broadcast from user id {self.user_id}!"
