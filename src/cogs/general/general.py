import discord.member
from discord import Role, app_commands, Interaction
from discord.ext import commands

from .general_cog import GeneralCog
from .messages.views.invite_view import InviteView
from .services import EmojiService, GuildService, MemberService, RoleService, ChannelService, MessageService
from src.kiyomi import Kiyomi, permissions
from ..settings.storage.model.emoji_setting import EmojiSetting


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
        async def register_member(member: discord.Member):
            self.member_service.register_member(member)
            self.member_service.register_guild_member(member.guild.id, member.id)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.guild_service.register_guild(guild.id)

        settings = [
            # TODO: Add bot owner permissions
            EmojiSetting.create(self.bot, "Invite button emoji", "invite_button_emoji"),
        ]

        self.bot.events.emit("setting_register", settings)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.guild_service.register_guild(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.guild_service.unregister_guild(guild.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.member_service.unregister_guild_member(member.guild.id, member.id)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        self.role_service.on_member_update(before, after)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        self.role_service.on_role_delete(role)

    @app_commands.command()
    async def invite(self, ctx: Interaction):
        """Get the invite link"""
        invite_view = InviteView(self.bot, ctx.guild)

        await invite_view.respond(ctx)

    @app_commands.command()
    async def ping(self, ctx: Interaction):
        """Kiyomi's ping to Discord servers"""
        await ctx.response.send_message(f"Ping is {round(self.bot.latency * 1000)} ms")

    @app_commands.command()
    @app_commands.describe(text="Text to repeat")
    @permissions.is_bot_owner_and_admin_guild()
    async def say(self, ctx: Interaction, text: str):
        """Kiyomi repeats what you say"""
        await ctx.response.defer()

        msg = await ctx.original_message()
        await msg.delete()

        await ctx.channel.send(text)
