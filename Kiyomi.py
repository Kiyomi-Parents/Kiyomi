import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.database import Database
from src.kiyomi.kiyomi import Kiyomi
from src.log import Logger

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

    # database.drop_tables()
    # database.create_tables()
    # database.create_schema_image()

    bot.run(TOKEN)
