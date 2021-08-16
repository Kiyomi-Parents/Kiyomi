from discord.ext import commands

from .tasks import Tasks
from .storage.uow import UnitOfWork
from src.base.base_cog import BaseCog
from src.cogs.security import Security


class AchievementRoles(BaseCog):
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    @commands.command()
    @Security.owner_or_permissions()
    async def enable_pp_roles(self, ctx):
        settings = self.uow.bot.get_cog("SettingsAPI")

        settings.set(ctx.guild.id, "achievement_roles_pp", True)

    @commands.command()
    @Security.owner_or_permissions()
    async def disable_pp_roles(self, ctx):
        settings = self.uow.bot.get_cog("SettingsAPI")

        settings.set(ctx.guild.id, "achievement_roles_pp", False)
