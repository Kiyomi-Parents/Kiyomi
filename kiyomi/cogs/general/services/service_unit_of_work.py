from .guild_member_service import GuildMemberService
from .guild_service import GuildService
from .channel_service import ChannelService
from .role_service import RoleService
from .member_service import MemberService
from .emoji_service import EmojiService
from .message_service import MessageService
from ..storage import StorageUnitOfWork
from kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.channels = ChannelService(bot, storage_uow.channels, storage_uow)
        self.emojis = EmojiService(bot, storage_uow.emojis, storage_uow)
        self.guilds = GuildService(bot, storage_uow.guilds, storage_uow)
        self.members = MemberService(bot, storage_uow.members, storage_uow)
        self.guild_members = GuildMemberService(bot, storage_uow.guild_members, storage_uow)
        self.messages = MessageService(bot, storage_uow.messages, storage_uow)
        self.roles = RoleService(bot, storage_uow.roles, storage_uow)
