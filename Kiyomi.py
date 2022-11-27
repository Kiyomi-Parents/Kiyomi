import asyncio
import logging.handlers
import os
import platform
import sys
from asyncio import AbstractEventLoop
from logging import StreamHandler

import discord

from kiyomi import ConsoleFormatter, FileFormatter, Database, Kiyomi, Config


async def startup(loop: AbstractEventLoop):
    discord_token = Config.get().Discord.Token
    database_host = Config.get().Database.Host
    database_user = Config.get().Database.User
    database_password = Config.get().Database.Password
    database_name = Config.get().Database.Name

    # Init database
    database = Database(
        f"mariadb+asyncmy://{database_user}:{database_password}@{database_host}/{database_name}?charset=utf8mb4"
    )

    await database.init()

    async with Kiyomi(command_prefix="!?#!a'", db=database, loop=loop) as bot:
        default_guild = Config.get().Discord.Guilds.Default
        if default_guild is not None:
            bot.default_guild = discord.Object(id=int(default_guild))

        debug_guilds = Config.get().Discord.Guilds.Debug
        if debug_guilds is not None and len(debug_guilds) > 0:
            bot.debug_guilds = [discord.Object(id=int(guild_id)) for guild_id in debug_guilds if guild_id]

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
