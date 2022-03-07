from discord.ext import commands

from src.kiyomi.base_cog import BaseCog
from .storage.uow import UnitOfWork
from .tasks import Tasks
from src.cogs.settings.storage.model.ToggleSetting import ToggleSetting


class AchievementRoles(BaseCog, name="Achievement Roles"):
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ToggleSetting.create("achievement_roles_pp", False)
        ]

        self.uow.bot.events.emit("setting_register", settings)
