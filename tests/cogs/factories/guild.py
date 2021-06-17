import pytest


@pytest.fixture
def guild_factory(bot):
    class Factory:
        @staticmethod
        def make(index):
            return bot.guilds[index]

    yield Factory()


@pytest.fixture
def guild(guild_factory):
    return guild_factory.make(0)
