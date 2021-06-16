# good bot.py
import os

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from dotenv import load_dotenv

from src.commands.errors import NoPrivateMessagesException
from src.log import Logger


class BSBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        Logger.log(bot.user.name, f'Connected to Discord!')

    async def global_block_dms(self, ctx):
        if ctx.guild is None:
            raise NoPrivateMessagesException("no")

        return True

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            await ctx.send(error)
        elif isinstance(error, NoPrivateMessagesException):
            await ctx.send(error)
        else:
            await ctx.send(f"Something went horribly wrong, check console!")
            raise error


if __name__ == '__main__':
    bot = BSBot(command_prefix="!")

    Logger.log_init()

    bot.load_extension(name="src.commands.beatsaber")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
