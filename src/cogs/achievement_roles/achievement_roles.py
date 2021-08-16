from discord.ext import commands

from .tasks import Tasks
from .storage.uow import UnitOfWork
from src.base.base_cog import BaseCog
from src.cogs.security import Security


class AchievementRoles(BaseCog):
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    @commands.group(invoke_without_command=True, name="pproles")
    @Security.owner_or_permissions(administrator=True)
    async def pp_roles(self, ctx):
        """PP role commands"""
        await ctx.send_help(ctx.command)

    @pp_roles.command(name="enable")
    @Security.owner_or_permissions()
    async def pp_roles_enable(self, ctx):
        """Enable pp roles"""
        settings = self.uow.bot.get_cog("SettingsAPI")

        settings.set(ctx.guild.id, "achievement_roles_pp", True)

    @pp_roles.command(name="disable")
    @Security.owner_or_permissions()
    async def pp_roles_disable(self, ctx):
        """Disable pp roles"""
        settings = self.uow.bot.get_cog("SettingsAPI")

        settings.set(ctx.guild.id, "achievement_roles_pp", False)
