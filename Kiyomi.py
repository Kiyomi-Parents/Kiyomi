import asyncio
import logging.handlers
import os
import platform
import sys
from asyncio import AbstractEventLoop
from logging import StreamHandler

import discord
from dotenv import load_dotenv

from kiyomi import ConsoleFormatter, FileFormatter, Database, Kiyomi


async def startup(loop: AbstractEventLoop):
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
        if default_guild is not None and len(default_guild) > 0:
            bot.default_guild = discord.Object(id=int(default_guild))

        debug_guilds = os.getenv("DEBUG_GUILDS")
        if debug_guilds is not None and len(debug_guilds) > 0:
            bot.debug_guilds = [discord.Object(id=int(guild_id)) for guild_id in debug_guilds.split(",") if guild_id]

        # Base Cogs
        await bot.load_extension(name="kiyomi.cogs.view_persistence")

        # General Function Cogs
        await bot.load_extension(name="kiyomi.cogs.general")
        await bot.load_extension(name="kiyomi.cogs.settings")
        await bot.load_extension(name="kiyomi.cogs.fancy_presence")

        # Function Cogs

        await bot.load_extension(name="kiyomi.cogs.scoresaber")
        await bot.load_extension(name="kiyomi.cogs.beatsaver")
        await bot.load_extension(name="kiyomi.cogs.leaderboard")
        await bot.load_extension(name="kiyomi.cogs.score_feed")
        await bot.load_extension(name="kiyomi.cogs.achievement")
        await bot.load_extension(name="kiyomi.cogs.achievement_roles")
        await bot.load_extension(name="kiyomi.cogs.emoji_echo")
        await bot.load_extension(name="kiyomi.cogs.twitch")
        await bot.load_extension(name="kiyomi.cogs.pfp_switcher")

        # await database.drop_tables()
        # await database.create_tables()

        await bot.start(token=discord_token)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler(
            filename='kiyomi.log',
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
    )
    file_handler.setFormatter(FileFormatter())
    logger.addHandler(file_handler)

    stdout_handler = StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ConsoleFormatter())
    logger.addHandler(stdout_handler)

    loop = None

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

    try:
        asyncio.run(startup(loop=loop))
    except KeyboardInterrupt:
        pass
