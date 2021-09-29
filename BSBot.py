import os

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands.errors import BadArgument
from dotenv import load_dotenv

from src.cogs.errors import NoPrivateMessagesException
from src.log import Logger
import json

class BSBot(commands.Bot):
    running_tests = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_check(self.global_block_dms)

    async def on_ready(self):
        Logger.log(self.user.name, "Connected to Discord!")

    @staticmethod
    def global_block_dms(ctx):
        if ctx.guild is None:
            raise NoPrivateMessagesException("no")

        return True

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return

        if isinstance(exception, MissingRequiredArgument):
            await context.send_help(context.command)
            await context.send(exception)
        elif isinstance(exception, NoPrivateMessagesException):
            await context.send(exception)
        elif isinstance(exception, BadArgument):
            await context.send("I don't understand what you're trying to do (bad argument)")
        else:
            await context.send("Something went horribly wrong, check console!")
            raise exception


if __name__ == "__main__":
    bot = BSBot(command_prefix="!")

    Logger.log_init()

    bot.load_extension(name="src.cogs.general")
    bot.load_extension(name="src.cogs.beatsaber")

    with open('config.json', 'r') as myfile:
    	data=myfile.read()
    data = json.loads(data)	
    TOKEN = str(data["token"])
    bot.run(TOKEN)
