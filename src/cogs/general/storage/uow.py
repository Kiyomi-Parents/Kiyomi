from sqlalchemy.orm import Session

from .repository.channel_repository import ChannelRepository
from .repository.emoji_repository import EmojiRepository
from .repository.guild_member_repository import GuildMemberRepository
from .repository.guild_repository import GuildRepository
from .repository.member_repository import MemberRepository
from .repository.member_role_repository import MemberRoleRepository
from .repository.role_repository import RoleRepository
from src.kiyomi.database import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.guild_repo = GuildRepository(session)
        self.channel_repo = ChannelRepository(session)
        self.role_repo = RoleRepository(session)
        self.member_repo = MemberRepository(session)
        self.guild_member_repo = GuildMemberRepository(session)
        self.member_role_repo = MemberRoleRepository(session)
        self.emoji_repo = EmojiRepository(session)
