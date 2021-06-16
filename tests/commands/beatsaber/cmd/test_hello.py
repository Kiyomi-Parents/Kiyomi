import pytest
from discord.ext.test import message, verify


@pytest.mark.asyncio
async def test_hello(bot):
    await message("!hello")
    assert verify() \
        .message() \
        .content("Hello there!")
