import pytest
from discord.ext.test import message, verify


@pytest.mark.asyncio
async def test_admin_test(bot):
    await message("!admintest")
    assert verify().message().contains().content("admintest")
