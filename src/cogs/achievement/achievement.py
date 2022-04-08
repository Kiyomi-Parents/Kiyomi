import discord
from discord import SlashCommandGroup, Option

from .achievement_cog import AchievementCog
from .messages.embeds.player_achievements import PlayerAchievementsEmbed


class Achievements(AchievementCog):
    achievements = SlashCommandGroup(
            "achievements",
            "Achievement commands"
    )

    @achievements.command(name="all")
    async def achievements_all(self, ctx: discord.ApplicationContext):
        """Show all achievements"""
        achievements = self.user_achievement_service.get_all_achievements(ctx.author.id)

        await ctx.respond(embed=PlayerAchievementsEmbed(self.bot, achievements))

    @achievements.command(name="complete")
    async def achievements_complete(self, ctx: discord.ApplicationContext):
        """Show all completed achievements"""
        achievements = self.user_achievement_service.get_all_completed_achievements(ctx.author.id)

        await ctx.respond(embed=PlayerAchievementsEmbed(self.bot, achievements))

    @achievements.command(name="uncomplete")
    async def achievements_uncomplete(self, ctx: discord.ApplicationContext):
        """Show all uncompleted achievements"""
        achievements = self.user_achievement_service.get_all_uncompleted_achievements(ctx.author.id)

        await ctx.respond(embed=PlayerAchievementsEmbed(self.bot, achievements))

    # Workaround
    async def get_all_groups(self, ctx: discord.AutocompleteContext):
        return await self.user_achievement_service.get_all_groups(ctx)

    @achievements.command(name="group")
    async def achievements_group(
            self,
            ctx: discord.ApplicationContext,
            group: Option(
                    str,
                    "Choose an achievement group",
                    autocomplete=get_all_groups
            )
    ):
        """Show all uncompleted achievements"""
        achievements = self.user_achievement_service.get_group_achievements(group, ctx.author.id)

        await ctx.respond(embed=PlayerAchievementsEmbed(self.bot, achievements))
