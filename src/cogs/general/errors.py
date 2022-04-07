from src.kiyomi.errors import CogException


class GeneralCogException(CogException):
    pass


class GuildNotFoundException(GeneralCogException):
    pass


class ChannelNotFoundException(GeneralCogException):
    pass


class MemberNotFoundException(GeneralCogException):
    pass


class RoleNotFoundException(GeneralCogException):
    pass


class EmojiAlreadyExistsException(GeneralCogException):
    pass


class EmojiNotFoundException(GeneralCogException):
    pass
