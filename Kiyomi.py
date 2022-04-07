import os

import discord
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.kiyomi import Kiyomi, Database
from src.log import Logger

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    DATABASE_IP = os.getenv("DATABASE_IP")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PW = os.getenv("DATABASE_PW")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # Init database
    database = Database(
            create_engine(
                    f"mariadb+pymysql://{DATABASE_USER}:{DATABASE_PW}@{DATABASE_IP}/{DATABASE_NAME}?charset=utf8mb4",
                    echo=False,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    connect_args={"connect_args": {"init_command": "SET time_zone = '+00:00'"}}
            )
    )

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = Kiyomi(command_prefix="!", intents=intents, db=database)

    default_guild = os.getenv("DEFAULT_GUILD")
    if default_guild is not None:
        bot.default_guild = int(default_guild)
        
    debug_guilds = os.getenv("DEBUG_GUILDS")
    if debug_guilds is not None:
        bot.debug_guilds = [int(guild_id) for guild_id in debug_guilds.split(",") if guild_id]

    Logger.log_init()

    bot.load_extension(name="src.cogs.general")
    bot.load_extension(name="src.cogs.settings")
    bot.load_extension(name="src.cogs.scoresaber")
    bot.load_extension(name="src.cogs.beatsaver")
    bot.load_extension(name="src.cogs.score_feed")
    bot.load_extension(name="src.cogs.leaderboard")
    bot.load_extension(name="src.cogs.achievement")
    bot.load_extension(name="src.cogs.achievement_roles")
    bot.load_extension(name="src.cogs.view_persistence")
    bot.load_extension(name="src.cogs.emoji_echo")
    bot.load_extension(name="src.cogs.fancy_presence")

    # database.drop_tables()
    # database.create_tables()
    # database.create_schema_image()

    bot.run(TOKEN)
