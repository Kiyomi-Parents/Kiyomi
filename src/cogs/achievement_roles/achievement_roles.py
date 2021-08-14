from discord.ext import commands

from .tasks import Tasks
from .storage.uow import UnitOfWork


class AchievementRoles(commands.Cog):
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    @commands.command()
    async def enable_pp_roles(self, ctx):
        settings = self.uow.bot.get_cog("SettingsAPI")

        settings.set(ctx.guild.id, "achievement_roles_pp", True)

    @commands.command()
    async def disable_pp_roles(self, ctx):
        settings = self.uow.bot.get_cog("SettingsAPI")

        settings.set(ctx.guild.id, "achievement_roles_pp", False)

    @commands.command()
    async def run_task(self, ctx):
        await self.tasks.update_member_roles()
