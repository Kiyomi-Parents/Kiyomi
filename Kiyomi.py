import os

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands.errors import BadArgument
from dotenv import load_dotenv
from pyee import AsyncIOEventEmitter
from sqlalchemy import create_engine

from src.cogs.errors import NoPrivateMessagesException
from src.database import Database
from src.log import Logger


class Kiyomi(commands.Bot):
    running_tests = False
    events = AsyncIOEventEmitter()
    running_tasks = []
    activity_list = ["sleeping", "sitting in a tiny box", "chilling @ Smugle Stick"]

    def __init__(self, *args, db: Database, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_check(self.global_block_dms)
        self.database = db

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
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    DATABASE_IP = os.getenv("DATABASE_IP")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PW = os.getenv("DATABASE_PW")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # Init database
    database = Database(create_engine(f"mariadb+pymysql://{DATABASE_USER}:{DATABASE_PW}@{DATABASE_IP}/{DATABASE_NAME}?charset=utf8mb4", echo=False, pool_pre_ping=True, pool_recycle=3600))

    bot = Kiyomi(command_prefix="!", db=database)

    Logger.log_init()

    bot.load_extension(name="src.cogs.general")
    bot.load_extension(name="src.cogs.settings")
    bot.load_extension(name="src.cogs.scoresaber")
    bot.load_extension(name="src.cogs.beatsaver")
    bot.load_extension(name="src.cogs.score_feed")
    bot.load_extension(name="src.cogs.leaderboard")
    bot.load_extension(name="src.cogs.achievements")
    bot.load_extension(name="src.cogs.achievement_roles")

    # database.create_tables()
    # database.create_schema_image()

    bot.run(TOKEN)
