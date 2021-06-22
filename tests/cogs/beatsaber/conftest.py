import pytest
from sqlalchemy import create_engine

from src.cogs.beatsaber.api.beatsaver import BeatSaver
from src.cogs.beatsaber.api.scoresaber import ScoreSaber
from src.cogs.beatsaber.actions import Actions
from src.cogs.beatsaber.beatsaber import BeatSaber
from src.cogs.beatsaber.tasks import Tasks
from src.cogs.beatsaber.storage.database import Database
from src.cogs.beatsaber.storage.uow import UnitOfWork
from tests.cogs.beatsaber.factories import *


@pytest.fixture(scope="session")
def scoresaber():
    return ScoreSaber()


@pytest.fixture(scope="session")
def beatsaver():
    return BeatSaver()


@pytest.fixture
def uow(bot, scoresaber, beatsaver):
    engine = create_engine("sqlite:///:memory:")
    database = Database(engine)

    return UnitOfWork(bot, database, scoresaber, beatsaver)


@pytest.fixture
def tasks(uow):
    return Tasks(uow)


@pytest.fixture
def actions(uow, tasks):
    return Actions(uow, tasks)


@pytest.fixture
def beatsaber_cog(uow, tasks, actions):
    return BeatSaber(uow, tasks, actions)


@pytest.fixture(autouse=True)
def add_cogs(bot, beatsaber_cog):
    bot.add_cog(beatsaber_cog)
