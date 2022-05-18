from src.kiyomi.error import CogException


class TwitchCogException(CogException):
    pass


class TwitchStreamerNotFound(TwitchCogException):
    def __init__(self, login: str):
        self.login = login

    def __str__(self):
        # TODO: fancy arg resolver
        return f"Couldn't find Twitch Streamer with {self.login}!"


class StreamNotFound(TwitchCogException):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        # TODO: fancy arg resolver
        return f"Couldn't find Twitch Stream from user id {self.user_id}!"
