from Kiyomi import Kiyomi
from .repository import GuildRepository, ChannelRepository, RoleRepository, MemberRepository, GuildMemberRepository, \
    MemberRoleRepository, EmojiRepository


class UnitOfWork:

    def __init__(self, bot: Kiyomi):
        self.guild_repo = GuildRepository(bot.database)
        self.channel_repo = ChannelRepository(bot.database)
        self.role_repo = RoleRepository(bot.database)
        self.member_repo = MemberRepository(bot.database)
        self.guild_member_repo = GuildMemberRepository(bot.database)
        self.member_role_repo = MemberRoleRepository(bot.database)
        self.emoji_repo = EmojiRepository(bot.database)

        self.bot = bot
