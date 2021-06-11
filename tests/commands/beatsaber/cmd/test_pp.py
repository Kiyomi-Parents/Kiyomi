import pytest
from discord.ext.test import message, verify_message, empty_queue


@pytest.mark.asyncio
async def test_show_pp(bot):
    await message("!player add 76561198029447509")
    await empty_queue()

    await message("!showpp")
    verify_message("PP is this big", contains=True)


@pytest.mark.asyncio
async def test_show_pp_no_profile(bot):
    await message("!showpp")
    verify_message("doesn't have a PP", contains=True)