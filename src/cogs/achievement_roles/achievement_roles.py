from discord.ext import commands

from src.cogs.settings.storage.model.toggle_setting import ToggleSetting
from .achievement_roles_cog import AchievementRolesCog


class AchievementRoles(AchievementRolesCog, name="Achievement Roles"):

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ToggleSetting.create("achievement_roles_pp", False)
        ]

        self.bot.events.emit("setting_register", settings)
