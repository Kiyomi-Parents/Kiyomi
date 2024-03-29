from kiyomi.error import CogException


class GeneralCogException(CogException):
    pass


class GuildNotFoundException(GeneralCogException):
    pass


class ChannelNotFoundException(GeneralCogException):
    pass


class MemberNotFoundException(GeneralCogException):
    pass


class RoleException(GeneralCogException):
    pass


class RoleNotFound(RoleException):
    def __init__(self, guild_id: int, role_id: int):
        self.guild_id = guild_id
        self.role_id = role_id

    def __str__(self):
        return f"Could not find Role %role_id% in Guild %guild_id%"


class FailedToCreateRole(RoleException):
    def __init__(self, guild_id: int, role_name: str, reason: str):
        self.guild_id = guild_id
        self.role_name = role_name
        self.reason = reason

    def __str__(self):
        return f"Failed to create Role {self.role_name} in Guild %guild_id% ({self.reason})"


class FailedToDeleteRole(RoleException):
    def __init__(self, guild_id: int, role_id: int, reason: str):
        self.guild_id = guild_id
        self.role_id = role_id
        self.reason = reason

    def __str__(self):
        return f"Failed to remove Role %role_id% from Guild %guild_id% ({self.reason})"


class FailedToAddToUser(RoleException):
    def __init__(self, guild_id: int, member_id: int, role_id: int, reason: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.role_id = role_id
        self.reason = reason

    def __str__(self):
        return f"Failed to add Role %role_id% to User %member_id% in Guild %guild_id% ({self.reason})"


class FailedToRemoveFromUser(RoleException):
    def __init__(self, guild_id: int, member_id: int, role_id: int, reason: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.role_id = role_id
        self.reason = reason

    def __str__(self):
        return f"Failed to remove Role %role_id% from User %member_id% in Guild %guild_id% " f"({self.reason})"


class EmojiAlreadyExistsException(GeneralCogException):
    pass


class EmojiNotFoundException(GeneralCogException):
    pass
