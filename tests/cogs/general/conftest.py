import pytest

from src.cogs.general import General


@pytest.fixture(autouse=True)
def add_cog(bot):
    bot.add_cog(General())
