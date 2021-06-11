import pytest
from discord.ext.commands import MissingRequiredArgument
from discord.ext.test import message, verify_message, empty_queue


@pytest.mark.asyncio
async def test_player(bot):
    await message("!player")
    verify_message("Type !help command for more info on a command.", contains=True)


@pytest.mark.asyncio
async def test_player_add(bot):
    await message("!player add 76561198029447509")
    verify_message("Successfully linked", contains=True)


@pytest.mark.asyncio
async def test_player_add_add(bot):
    await message("!player add 76561198029447509")
    verify_message("Successfully linked", contains=True)

    await message("!player add 76561198029447509")
    verify_message("has already been added!", contains=True)


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
    verify_message("Successfully linked", contains=True)

    await message("!player add 76561198029447509", channel=text_channel_b)
    verify_message("Successfully linked", contains=True)


@pytest.mark.asyncio
async def test_player_remove(bot):
    await message("!player add 76561198029447509")
    verify_message("Successfully linked", contains=True)

    await message("!player remove")
    verify_message("Successfully unlinked", contains=True)


@pytest.mark.asyncio
async def test_player_remove_empty(bot):
    await message("!player remove")
    verify_message("You don't have a ScoreSaber profile linked to yourself.")


@pytest.mark.asyncio
async def test_player_remove_multi_guild(guild_factory, text_channel_factory):
    guild_a = guild_factory.make(0)
    guild_b = guild_factory.make(1)

    text_channel_a = await text_channel_factory.make(guild_a)
    text_channel_b = await text_channel_factory.make(guild_b)

    await message("!player add 76561198029447509", channel=text_channel_a)
    verify_message("Successfully linked", contains=True)

    await message("!player add 76561198029447509", channel=text_channel_b)
    verify_message("Successfully linked", contains=True)

    await message("!player remove", channel=text_channel_a)
    verify_message("Successfully unlinked", contains=True)

    await message("!player remove", channel=text_channel_b)
    verify_message("Successfully unlinked", contains=True)
