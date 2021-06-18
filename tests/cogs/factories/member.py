import pytest
import discord.ext.test as dpytest


@pytest.fixture
def member_factory(guild):
    class Factory:
        @staticmethod
        async def make():
            member_count = len(guild.members)

            await dpytest.member_join()
            return guild.members[member_count]

    yield Factory()


@pytest.fixture
async def member(member_factory):
    return await member_factory.make()