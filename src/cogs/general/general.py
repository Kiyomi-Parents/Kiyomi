import discord.member
from discord import Role
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
        super().__init__(
                bot,
                emoji_service,
                guild_service,
                member_service,
                channel_service,
                message_service,
                role_service
        )

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

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        self.role_service.on_member_update(before, after)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        self.role_service.on_role_delete(role)

    @commands.slash_command()
    async def invite(self, ctx):
        """Get the invite link for the bot"""
        await ctx.respond(
                "https://discord.com/api/oauth2/authorize?client_id=834048194085650462&permissions=139855260736&scope=bot%20applications.commands",
                ephemeral=True
        )

    @commands.slash_command()
    async def hello(self, ctx):
        """Greet the bot"""
        await ctx.respond("Hello there!")

    @commands.slash_command(**permissions.is_bot_owner())
    async def say(self, ctx, text: str):
        """I repeat what you say"""
        await ctx.respond(text)
