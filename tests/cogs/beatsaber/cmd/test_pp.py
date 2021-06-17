import pytest
from discord.ext.test import message, verify, empty_queue


@pytest.mark.asyncio
async def test_show_pp(bot):
    await message("!player add 76561198029447509")
    await empty_queue()

    await message("!showpp")
    assert verify() \
        .message() \
        .contains() \
        .content("PP is this big")


@pytest.mark.asyncio
async def test_show_pp_no_profile(bot):
    await message("!showpp")
    assert verify() \
        .message() \
        .contains() \
        .content("doesn't have a PP")
