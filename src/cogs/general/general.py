import discord.member
from discord.ext import commands

from .general_cog import GeneralCog
from .services import EmojiService, GuildService, MemberService, RoleService, ChannelService, MessageService
from src.kiyomi import Kiyomi, permissions


class General(GeneralCog):
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
        super().__init__(bot, emoji_service, guild_service, member_service, channel_service, message_service, role_service)

        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("register_member")
        async def register_member(discord_member: discord.Member):
            self.member_service.register_member(discord_member)
            self.member_service.register_guild_member(discord_member)

    @commands.Cog.listener()
    async def on_ready(self):
        for discord_guild in self.bot.guilds:
            await self.guild_service.register_guild(discord_guild.id)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.guild_service.register_guild(guild.id)

    @commands.slash_command()
    async def hello(self, ctx):
        """Greet the bot"""
        await ctx.respond("Hello there!")

    @commands.slash_command(**permissions.is_bot_owner())
    async def say(self, ctx, text: str):
        """I repeat what you say"""
        await ctx.respond(text)
