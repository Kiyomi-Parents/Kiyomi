import pytest
from discord.ext.test import message, verify_message


@pytest.mark.asyncio
async def test_hello(bot):
    await message("!hello")
    verify_message("Hello there!")
