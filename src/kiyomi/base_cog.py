from discord import ApplicationContext, ApplicationCommandInvokeError
from discord.ext import commands
from termcolor import colored

from .error import KiyomiException, CogException
from .kiyomi import Kiyomi
from src.log import Logger


class BaseCog(commands.Cog):
    def __init__(self, bot: Kiyomi):
        self.bot = bot

    async def cog_before_invoke(self, ctx: ApplicationContext):
        command_args = [f"{item['name']}: {item['value']}" for item in ctx.interaction.data['options']]

        Logger.log(
                self.qualified_name,
                f"{colored(ctx.interaction.user.name, 'blue')} executed command "
                f"{colored('/' + ctx.command.qualified_name, 'blue')} "
                f"{colored(''.join(command_args), 'cyan')} in "
                f"{colored(f'#{ctx.interaction.channel.name}', 'blue')} at "
                f"{colored(ctx.interaction.guild.name, 'blue')}"
        )

        await ctx.trigger_typing()

    async def cog_command_error(self, ctx: ApplicationContext, exception: Exception):
        if isinstance(exception, ApplicationCommandInvokeError):
            error = exception.original

            if isinstance(error, KiyomiException):
                if error.is_handled:
                    return

            if isinstance(error, CogException):
                return await error.handle(ctx=ctx, bot=self.bot)
