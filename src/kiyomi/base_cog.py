from discord.ext import commands
from termcolor import colored

from src.log import Logger


class BaseCog(commands.Cog):
    async def cog_before_invoke(self, ctx):
        Logger.log(self.qualified_name,
                   f"{colored(ctx.author.name, 'blue')} executed command "
                   f"{colored(ctx.message.content, 'blue')} in "
                   f"{colored(ctx.channel.name, 'blue')} at "
                   f"{colored(ctx.guild.name, 'blue')}")

        await ctx.trigger_typing()
