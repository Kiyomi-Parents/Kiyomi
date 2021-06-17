import pytest
from discord.ext.commands import MissingRequiredArgument
from discord.ext.test import message, verify, empty_queue


@pytest.mark.asyncio
async def test_player(bot):
    await message("!player")
    assert verify() \
        .message() \
        .contains() \
        .content("Type !help command for more info on a command.")


@pytest.mark.asyncio
async def test_player_add(bot):
    await message("!player add 76561198029447509")
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")


@pytest.mark.asyncio
async def test_player_add_add(bot):
    await message("!player add 76561198029447509")
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message("!player add 76561198029447509")
    assert verify() \
        .message() \
        .contains() \
        .content("has already been added!")


@pytest.mark.asyncio
async def test_player_add_empty(bot):
    with pytest.raises(MissingRequiredArgument):
        await message("!player add")
    await empty_queue()


@pytest.mark.asyncio
async def test_player_add_multi_guild(guild_factory, text_channel_factory):
    guild_a = guild_factory.make(0)
    guild_b = guild_factory.make(1)

    text_channel_a = await text_channel_factory.make(guild_a)
    text_channel_b = await text_channel_factory.make(guild_b)

    await message("!player add 76561198029447509", channel=text_channel_a)
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message("!player add 76561198029447509", channel=text_channel_b)
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")


@pytest.mark.asyncio
async def test_player_remove(bot):
    await message("!player add 76561198029447509")
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message("!player remove")
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully unlinked")


@pytest.mark.asyncio
async def test_player_remove_empty(bot):
    await message("!player remove")
    assert verify() \
        .message() \
        .content("You don't have a ScoreSaber profile linked to yourself.")


@pytest.mark.asyncio
async def test_player_remove_multi_guild(guild_factory, text_channel_factory):
    guild_a = guild_factory.make(0)
    guild_b = guild_factory.make(1)

    text_channel_a = await text_channel_factory.make(guild_a)
    text_channel_b = await text_channel_factory.make(guild_b)

    await message("!player add 76561198029447509", channel=text_channel_a)
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message("!player add 76561198029447509", channel=text_channel_b)
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message("!player remove", channel=text_channel_a)
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully unlinked")

    await message("!player remove", channel=text_channel_b)
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully unlinked")
