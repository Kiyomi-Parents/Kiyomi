import discord.member
from discord import Role, app_commands, Interaction
from discord.ext import commands

from .messages.views.invite_view import InviteView
from .services import (
    ServiceUnitOfWork,
)
from kiyomi import permissions, BaseCog
from ..settings.storage.model.emoji_setting import EmojiSetting


class General(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        @self.bot.events.on("register_member")
        async def register_member(member: discord.Member):
            discord_guild = await self.service_uow.guilds.register_guild(member.guild)
            await self.service_uow.members.register_member(discord_guild, member.id)
            await self.service_uow.members.register_guild_member(member.guild.id, member.id)
            await self.service_uow.save_changes()
            await self.service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.service_uow.guilds.register_guilds(self.bot.guilds)
        await self.service_uow.save_changes()
        await self.service_uow.close()

        settings = [
            # TODO: Add bot owner permissions
            EmojiSetting.create(self.bot, "Invite button emoji", "invite_button_emoji"),
            EmojiSetting.create(self.bot, "ScoreSaber emoji", "scoresaber_emoji"),
        ]

        self.bot.events.emit("setting_register", settings)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.service_uow.guilds.register_guild(guild)
        await self.service_uow.save_changes()
        await self.service_uow.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.service_uow.guilds.unregister_guild(guild.id)
        await self.service_uow.save_changes()
        await self.service_uow.close()

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        await self.service_uow.guilds.register_guild(after)
        await self.service_uow.save_changes()
        await self.service_uow.close()

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.service_uow.members.unregister_guild_member(member.guild.id, member.id)
        await self.service_uow.save_changes()
        await self.service_uow.close()

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        await self.service_uow.roles.on_member_update(before, after)
        await self.service_uow.save_changes()
        await self.service_uow.close()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        await self.service_uow.roles.on_role_delete(role)
        await self.service_uow.save_changes()
        await self.service_uow.close()

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
        await ctx.response.defer(ephemeral=True)

        msg = await ctx.original_message()
        await msg.delete()

        await ctx.channel.send(text)
