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
