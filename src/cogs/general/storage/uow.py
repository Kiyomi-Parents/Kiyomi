from sqlalchemy.orm import Session

from src.database import BaseUnitOfWork
from .repository import GuildRepository, ChannelRepository, RoleRepository, MemberRepository, GuildMemberRepository, \
    MemberRoleRepository, EmojiRepository


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
