from src.kiyomi import BaseCog, Kiyomi
from .services import EmojiService, GuildService, MemberService, RoleService


class GeneralCog(BaseCog):
    def __init__(self,
        bot: Kiyomi,
        emoji_service: EmojiService,
        guild_service: GuildService,
        member_service: MemberService,
        role_service: RoleService
    ):
        super().__init__(bot)

        self.emoji_service = emoji_service
        self.guild_service = guild_service
        self.member_service = member_service
        self.role_service = role_service
