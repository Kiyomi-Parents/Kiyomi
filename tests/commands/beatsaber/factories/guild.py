import pytest


@pytest.fixture
def guild_factory(bot):
    class factory:
        @staticmethod
        def make(index):
            return bot.guilds[index]

    yield factory()


@pytest.fixture
def guild(guild_factory):
    return guild_factory.make(0)


@pytest.fixture
def db_guild_factory(uow):
    class factory:
        @staticmethod
        def make(guild):
            return uow.guild_repo.add_guild(guild)

    yield factory()


@pytest.fixture
def db_guild(guild, db_guild_factory):
    return db_guild_factory.make(guild)
