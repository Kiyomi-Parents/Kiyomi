import asyncio
import os
import platform
from asyncio import AbstractEventLoop

import discord
from dotenv import load_dotenv

from src.kiyomi import Kiyomi, Database
from src.log import Logger


async def startup(loop: AbstractEventLoop):
    Logger.log_init()

    load_dotenv()
    discord_token = os.getenv("DISCORD_TOKEN")
    database_ip = os.getenv("DATABASE_IP")
    database_user = os.getenv("DATABASE_USER")
    database_password = os.getenv("DATABASE_PW")
    database_name = os.getenv("DATABASE_NAME")

    # Init database
    database = Database(
            f"mariadb+asyncmy://{database_user}:{database_password}@{database_ip}/{database_name}?charset=utf8mb4"
    )

    await database.init()

    async with Kiyomi(command_prefix="!", db=database, loop=loop) as bot:
        default_guild = os.getenv("DEFAULT_GUILD")
        if default_guild is not None:
            bot.default_guild = discord.Object(id=int(default_guild))

        debug_guilds = os.getenv("DEBUG_GUILDS")
        if debug_guilds is not None:
            bot.debug_guilds = [discord.Object(id=int(guild_id)) for guild_id in debug_guilds.split(",") if guild_id]

        # Base Cogs
        await bot.load_extension(name="src.cogs.view_persistence")

        # General Function Cogs
        await bot.load_extension(name="src.cogs.general")
        await bot.load_extension(name="src.cogs.settings")
        await bot.load_extension(name="src.cogs.fancy_presence")

        # Function Cogs

        await bot.load_extension(name="src.cogs.scoresaber")
        await bot.load_extension(name="src.cogs.beatsaver")
        await bot.load_extension(name="src.cogs.leaderboard")
        await bot.load_extension(name="src.cogs.score_feed")
        await bot.load_extension(name="src.cogs.achievement")
        await bot.load_extension(name="src.cogs.achievement_roles")
        await bot.load_extension(name="src.cogs.emoji_echo")
        await bot.load_extension(name="src.cogs.pfp_switcher")

        # await database.drop_tables()
        # await database.create_tables()

        await bot.start(token=discord_token)


if __name__ == "__main__":
    loop = None

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

    try:
        asyncio.run(startup(loop=loop))
    except KeyboardInterrupt:
        pass
