from discord import ApplicationContext
from discord.ext import commands
from termcolor import colored

from .kiyomi import Kiyomi
from src.log import Logger


class BaseCog(commands.Cog):
    def __init__(self, bot: Kiyomi):
        self.bot = bot

    async def cog_before_invoke(self, ctx: ApplicationContext):
        Logger.log(self.qualified_name,
                   f"{colored(ctx.interaction.user.name, 'blue')} executed command "
                   f"{colored('/' + ctx.command.qualified_name, 'blue')} in "
                   f"{colored(ctx.interaction.channel.name, 'blue')} at "
                   f"{colored(ctx.interaction.guild.name, 'blue')}")

        await ctx.trigger_typing()
