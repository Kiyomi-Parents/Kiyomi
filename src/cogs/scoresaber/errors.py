from typing import Optional

from src.kiyomi.error import CogException


class ScoreSaberCogException(CogException):
    pass


class MemberUsingDifferentPlayerAlreadyException(ScoreSaberCogException):
    def __init__(self, member_id: int, player_id: str):
        self.member_id = member_id
        self.player_id = player_id

    def __str__(self):
        return ("You are linked as %player_id% in another guild!\n"
                "You can't have different Score Saber profiles in different guilds!")


class PlayerRegisteredInGuildAlreadyException(ScoreSaberCogException):
    def __init__(self, guild_id: int, player_id: str):
        self.guild_id = guild_id
        self.player_id = player_id

    def __str__(self):
        return f"Player %player_id% has already been registered in this guild!"


class MemberHasPlayerAlreadyRegisteredInGuildException(ScoreSaberCogException):
    def __init__(self, guild_id: int, member_id: int, player_id: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.player_id = player_id

    def __str__(self):
        return f"You have already added yourself as %player_id%!"


class MemberPlayerNotFoundInGuildException(ScoreSaberCogException):
    def __init__(self, guild_id: int, member_id: int, player_id: Optional[str] = None):
        self.guild_id = guild_id
        self.member_id = member_id
        self.player_id = player_id

    def __str__(self):
        return f"You don't have a ScoreSaber profile linked to yourself."


class PlayerNotFoundException(ScoreSaberCogException):
    def __init__(self, player_id: str):
        self.player_id = player_id

    def __str__(self):
        return f"Couldn't find Score Saber profile with ID %player_id%!"
