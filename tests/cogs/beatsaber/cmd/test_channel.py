import pytest
from discord.ext.test import message, verify


@pytest.mark.asyncio
async def test_channel(bot):
    await message("!channel")
    assert verify()\
        .message()\
        .contains()\
        .content("Type !help command for more info on a command.")


@pytest.mark.asyncio
async def test_channel_add(text_channel):
    await message("!channel add", channel=text_channel)
    assert verify()\
        .message()\
        .contains()\
        .content(f"Channel **{text_channel.name}** has successfully set as the notification channel!")


@pytest.mark.asyncio
async def test_channel_remove(text_channel):
    await message("!channel remove", channel=text_channel)
    assert verify()\
        .message()\
        .contains()\
        .content("There isn't a notification channel set for this Discord server.")


@pytest.mark.asyncio
async def test_channel_add_remove(text_channel):
    await message("!channel add", channel=text_channel)
    assert verify()\
        .message()\
        .contains()\
        .content(f"Channel **{text_channel.name}** has successfully set as the notification channel!")

    await message("!channel remove", channel=text_channel)
    assert verify()\
        .message()\
        .contains()\
        .content("Notifications channel successfully removed!")


@pytest.mark.asyncio
async def test_channel_add_add(text_channel):
    await message("!channel add", channel=text_channel)
    assert verify()\
        .message()\
        .contains()\
        .content(f"Channel **{text_channel.name}** has successfully set as the notification channel!")

    await message("!channel add", channel=text_channel)
    assert verify()\
        .message()\
        .contains()\
        .content(f"Channel **{text_channel.name}** has already been set as the notification channel!")


@pytest.mark.asyncio
async def test_channel_add_add_different(text_channel_factory):
    text_channel_a = await text_channel_factory.make()
    text_channel_b = await text_channel_factory.make()

    await message("!channel add", channel=text_channel_a)
    assert verify()\
        .message()\
        .contains()\
        .content(f"Channel **{text_channel_a.name}** has successfully set as the notification channel!")

    await message("!channel add", channel=text_channel_b)
    assert verify()\
        .message()\
        .contains()\
        .content(f"Channel **{text_channel_a.name}** has already been set as the notification channel!")
