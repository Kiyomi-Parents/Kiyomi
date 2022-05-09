from typing import List

from discord import app_commands, Interaction
from discord.app_commands import Choice

from .achievement_cog import AchievementCog
from .messages.embeds.player_achievements import PlayerAchievementsEmbed
from src.kiyomi import Utils


class Achievements(AchievementCog):
    achievements = app_commands.Group(
            name="achievements",
            description="Achievement commands"
    )

    @achievements.command(name="all")
    async def achievements_all(self, ctx: Interaction):
        """Show all achievements"""
        achievements = self.user_achievement_service.get_all_achievements(ctx.user.id)

        await ctx.response.send_message(embed=PlayerAchievementsEmbed(self.bot, achievements))

    @achievements.command(name="complete")
    async def achievements_complete(self, ctx: Interaction):
        """Show all completed achievements"""
        achievements = self.user_achievement_service.get_all_completed_achievements(ctx.user.id)

        await ctx.response.send_message(embed=PlayerAchievementsEmbed(self.bot, achievements))

    @achievements.command(name="uncomplete")
    async def achievements_uncomplete(self, ctx: Interaction):
        """Show all uncompleted achievements"""
        achievements = self.user_achievement_service.get_all_uncompleted_achievements(ctx.user.id)

        await ctx.response.send_message(embed=PlayerAchievementsEmbed(self.bot, achievements))

    @achievements.command(name="group")
    @app_commands.describe(group="Choose an achievement group")
    async def achievements_group(self, ctx: Interaction, group: str):
        """Show all uncompleted achievements"""
        achievements = self.user_achievement_service.get_group_achievements(group, ctx.user.id)

        await ctx.response.send_message(embed=PlayerAchievementsEmbed(self.bot, achievements))

    @achievements_group.autocomplete("group")
    async def get_all_groups(self, ctx: Interaction, current: str) -> List[Choice[str]]:
        choices = await self.user_achievement_service.get_all_groups(ctx, current)

        return Utils.limit_list(choices, 25)
