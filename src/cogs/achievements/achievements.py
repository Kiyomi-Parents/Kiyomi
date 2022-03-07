import discord
from discord import SlashCommandGroup, Option

from src.kiyomi.base_cog import BaseCog
from .actions import Actions
from .message import Message
from .storage.uow import UnitOfWork


class Achievements(BaseCog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    achievements = SlashCommandGroup(
        "achievements",
        "Achievement commands"
    )

    @achievements.command(name="all")
    async def achievements_all(self, ctx: discord.ApplicationContext):
        """Show all achievements"""
        achievements = self.actions.get_all_achievements(ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.respond(embed=achievement_embed)

    @achievements.command(name="complete")
    async def achievements_complete(self, ctx: discord.ApplicationContext):
        """Show all completed achievements"""
        achievements = self.actions.get_all_completed_achievements(ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.respond(embed=achievement_embed)

    @achievements.command(name="uncomplete")
    async def achievements_uncomplete(self, ctx: discord.ApplicationContext):
        """Show all uncompleted achievements"""
        achievements = self.actions.get_all_uncompleted_achievements(ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.respond(embed=achievement_embed)

    # Workaround
    async def get_all_groups(self, ctx: discord.AutocompleteContext):
        return await self.actions.get_all_groups(ctx)

    @achievements.command(name="group")
    async def achievements_group(self,
        ctx: discord.ApplicationContext,
        group: Option(
            str,
            "Choose an achievement group",
            autocomplete=get_all_groups
        )
    ):
        """Show all uncompleted achievements"""
        achievements = self.actions.get_group_achievements(group, ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.respond(embed=achievement_embed)
