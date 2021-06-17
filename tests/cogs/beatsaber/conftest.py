import glob
import os

import discord
import discord.ext.test as dpytest
from sqlalchemy import create_engine

from BSBot import BSBot
from src.api import ScoreSaber, BeatSaver
from src.cogs.beatsaber.actions import Actions
from src.cogs.beatsaber.beatsaber import BeatSaber
from src.cogs.beatsaber.tasks import Tasks
from src.cogs.general import General
from src.storage.database import Database
from src.storage.uow import UnitOfWork
from tests.cogs import *
from .factories import *


@pytest.fixture
def pre_bot(event_loop):
    intents = discord.Intents.default()
    intents.members = True

    bot = BSBot("!", loop=event_loop, intents=intents)
    bot.running_tests = True

    return bot


@pytest.fixture(scope="session")
def scoresaber():
    return ScoreSaber()


@pytest.fixture(scope="session")
def beatsaver():
    return BeatSaver()


@pytest.fixture
def uow(pre_bot, scoresaber, beatsaver):
    engine = create_engine("sqlite:///:memory:")
    database = Database(engine)

    return UnitOfWork(pre_bot, database, scoresaber, beatsaver)


@pytest.fixture
def tasks(uow):
    return Tasks(uow)


@pytest.fixture
def actions(uow, tasks):
    return Actions(uow, tasks)


@pytest.fixture
def beatsaber_cog(uow, tasks, actions):
    return BeatSaber(uow, tasks, actions)


@pytest.fixture
def bot(pre_bot, beatsaber_cog):
    pre_bot.add_cog(beatsaber_cog)
    pre_bot.add_cog(General())

    dpytest.configure(pre_bot, num_guilds=2, num_channels=1, num_members=1)
    return pre_bot


def pytest_sessionfinish():
    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    file_list = glob.glob("./dpytest_*.dat")
    for file_path in file_list:
        try:
            os.remove(file_path)
        except Exception:
            print(f"Error while deleting file: {file_path}")
