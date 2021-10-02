import glob
import os

import discord
import discord.ext.test as dpytest
import pytest

from Kiyomi import Kiyomi
from tests.cogs.factories import *


@pytest.fixture
def bot(event_loop):
    intents = discord.Intents.default()
    intents.members = True

    bot = Kiyomi("!", loop=event_loop, intents=intents)
    bot.running_tests = True

    dpytest.configure(bot, num_guilds=2, num_channels=1, num_members=1)
    return bot


def pytest_sessionfinish():
    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    file_list = glob.glob('./dpytest_*.dat')
    for file_path in file_list:
        try:
            os.remove(file_path)
        except Exception:
            print("Error while deleting file : ", file_path)
