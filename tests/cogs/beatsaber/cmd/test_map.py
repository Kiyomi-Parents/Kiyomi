import pytest
from discord.ext.test import message, verify


@pytest.mark.asyncio
async def test_map():
    await message("!map 194b4")
    assert not verify().message().nothing()

