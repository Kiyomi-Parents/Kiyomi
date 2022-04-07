from typing import Optional

from src.cogs.general.storage.model.guild import Guild
from src.cogs.general.storage.model.member import Member
from .storage.model.player import Player
from ...kiyomi.errors import CogException


class ScoreSaberCogException(CogException):
    pass


class GuildException(ScoreSaberCogException):
    def __init__(self, guild: Guild):
        self.guild = guild


class MemberException(ScoreSaberCogException):
    def __init__(self, member: Member):
        self.member = member


class PlayerException(ScoreSaberCogException):
    def __init__(self, player: Player):
        self.player = player


class MemberUsingDifferentPlayerAlreadyException(MemberException, PlayerException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f'''You are linked as **{self.player.name} in another guild!
        You can't have different Score Saber profiles in different guilds!'''


class PlayerRegisteredInGuildAlreadyException(GuildException, MemberException, PlayerException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"Player **{self.player.name}** has already been linked to **{self.member.name}** in this guild!"


class MemberHasPlayerAlreadyRegisteredInGuildException(GuildException, MemberException, PlayerException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"You have already added yourself as **{self.player.name}**!"


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
        return f"Couldn't find Score Saber profile with ID {self.player_id}!"
