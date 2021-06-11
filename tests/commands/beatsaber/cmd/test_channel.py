import pytest
from discord.ext.test import message, verify_message


@pytest.mark.asyncio
async def test_channel(bot):
    await message("!channel")
    verify_message("Type !help command for more info on a command.", contains=True)


@pytest.mark.asyncio
async def test_channel_add(text_channel):
    await message("!channel add", channel=text_channel)
    verify_message(f"Channel **{text_channel.name}** has successfully set as the notification channel!", contains=True)


@pytest.mark.asyncio
async def test_channel_remove(text_channel):
    await message("!channel remove", channel=text_channel)
    verify_message("There isn't a notification channel set for this Discord server.", contains=True)


@pytest.mark.asyncio
async def test_channel_add_remove(text_channel):
    await message("!channel add", channel=text_channel)
    verify_message(f"Channel **{text_channel.name}** has successfully set as the notification channel!", contains=True)

    await message("!channel remove", channel=text_channel)
    verify_message("Notifications channel successfully removed!", contains=True)


@pytest.mark.asyncio
async def test_channel_add_add(text_channel):
    await message("!channel add", channel=text_channel)
    verify_message(f"Channel **{text_channel.name}** has successfully set as the notification channel!", contains=True)

    await message("!channel add", channel=text_channel)
    verify_message(f"Channel **{text_channel.name}** has already been set as the notification channel!", contains=True)


@pytest.mark.asyncio
async def test_channel_add_add_different(text_channel_factory):
    text_channel_a = await text_channel_factory.make()
    text_channel_b = await text_channel_factory.make()

    await message("!channel add", channel=text_channel_a)
    verify_message(f"Channel **{text_channel_a.name}** has successfully set as the notification channel!", contains=True)

    await message("!channel add", channel=text_channel_b)
    verify_message(f"Channel **{text_channel_a.name}** has already been set as the notification channel!", contains=True)


