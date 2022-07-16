from sqlalchemy.ext.asyncio import AsyncSession

from .repository.channel_repository import ChannelRepository
from .repository.emoji_repository import EmojiRepository
from .repository.guild_member_repository import GuildMemberRepository
from .repository.guild_repository import GuildRepository
from .repository.member_repository import MemberRepository
from .repository.member_role_repository import MemberRoleRepository
from .repository.message_repository import MessageRepository
from .repository.role_repository import RoleRepository
from kiyomi.database import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.guilds = GuildRepository(self._session)
        self.channels = ChannelRepository(self._session)
        self.roles = RoleRepository(self._session)
        self.members = MemberRepository(self._session)
        self.guild_members = GuildMemberRepository(self._session)
        self.member_roles = MemberRoleRepository(self._session)
        self.emojis = EmojiRepository(self._session)
        self.messages = MessageRepository(self._session)
