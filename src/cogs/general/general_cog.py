from src.kiyomi import BaseCog, Kiyomi
from .services import EmojiService, GuildService, MemberService, RoleService, ChannelService, MessageService


class GeneralCog(BaseCog):
    def __init__(
            self,
            bot: Kiyomi,
            emoji_service: EmojiService,
            guild_service: GuildService,
            member_service: MemberService,
            channel_service: ChannelService,
            message_service: MessageService,
            role_service: RoleService
    ):
        super().__init__(bot)

        self.emoji_service = emoji_service
        self.guild_service = guild_service
        self.member_service = member_service
        self.channel_service = channel_service
        self.message_service = message_service
        self.role_service = role_service
