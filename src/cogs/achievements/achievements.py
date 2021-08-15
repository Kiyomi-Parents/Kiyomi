from discord.ext import commands

from .actions import Actions
from .message import Message
from .storage.uow import UnitOfWork
from src.base.base_cog import BaseCog


class Achievements(BaseCog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    @commands.group(invoke_without_command=True)
    async def achievements(self, ctx):
        """Achievement commands"""
        await ctx.send_help(ctx.command)

    @achievements.command(name="all")
    async def achievements_all(self, ctx):
        """Show all achievements"""
        achievements = self.actions.get_all_achievements(ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.send(embed=achievement_embed)

    @achievements.command(name="complete")
    async def achievements_complete(self, ctx):
        """Show all completed achievements"""
        achievements = self.actions.get_all_completed_achievements(ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.send(embed=achievement_embed)

    @achievements.command(name="uncomplete")
    async def achievements_uncomplete(self, ctx):
        """Show all uncompleted achievements"""
        achievements = self.actions.get_all_uncompleted_achievements(ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.send(embed=achievement_embed)

    @achievements.command(name="group")
    async def achievements_group(self, ctx, group: str):
        """Show all uncompleted achievements"""
        achievements = self.actions.get_group_achievements(group, ctx.author.id)
        achievement_embed = Message.get_achievements_embed(achievements)

        await ctx.send(embed=achievement_embed)
