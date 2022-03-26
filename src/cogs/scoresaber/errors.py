from typing import Optional

from src.cogs.general.storage.model.guild import Guild
from src.cogs.general.storage.model.member import Member
from .storage.model.player import Player


class ScoreSaberException(Exception):
    pass


class GuildException(ScoreSaberException):
    def __init__(self, guild: Guild):
        self.guild = guild


class MemberException(ScoreSaberException):
    def __init__(self, member: Member):
        self.member = member


class PlayerException(ScoreSaberException):
    def __init__(self, player: Player):
        self.player = player


class MemberUsingDifferentPlayerAlreadyException(MemberException, PlayerException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PlayerRegisteredInGuildAlreadyException(GuildException, MemberException, PlayerException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MemberHasPlayerAlreadyRegisteredInGuildException(GuildException, MemberException, PlayerException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MemberPlayerNotFoundInGuildException(ScoreSaberException):
    def __init__(self, guild_id: int, member_id: int, player_id: Optional[str] = None):
        self.guild_id = guild_id
        self.member_id = member_id
        self.player_id = player_id


class PlayerNotFoundException(ScoreSaberException):
    def __init__(self, player_id: str):
        self.player_id = player_id
