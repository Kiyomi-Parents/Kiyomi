import pytest
from discord.ext.test import message, verify_message


@pytest.mark.asyncio
async def test_admin_test(bot):
    await message("!admintest")
    verify_message("admintest", contains=True)
