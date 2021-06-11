import pytest
from discord.ext.commands import MissingRequiredArgument
from discord.ext.test import message, verify_message, empty_queue


def pytest_generate_tests(metafunc):
    if "feature_flag" in metafunc.fixturenames:
        metafunc.parametrize("feature_flag", ["pp_roles"], indirect=True)


@pytest.fixture
def feature_flag(request):
    return request.param


@pytest.mark.asyncio
async def test_feature(bot):
    await message("!feature")
    verify_message("Type !help command for more info on a command.", contains=True)


@pytest.mark.asyncio
async def test_feature_enable(bot):
    with pytest.raises(MissingRequiredArgument):
        await message("!feature enable")

    await empty_queue()


@pytest.mark.asyncio
async def test_feature_enable_feature_flag(bot, feature_flag):
    await message(f"!feature enable {feature_flag}")
    verify_message(f"Enabled {feature_flag} feature!")


@pytest.mark.asyncio
async def test_feature_enable_feature_flag_player(bot, feature_flag):
    await message(f"!player add 76561198029447509")
    verify_message("Successfully linked", contains=True)

    await message(f"!feature enable {feature_flag}")
    verify_message(f"Enabled {feature_flag} feature!")


@pytest.mark.asyncio
async def test_feature_enable_feature_flag_already_enabled(bot, feature_flag):
    await message(f"!feature enable {feature_flag}")
    verify_message(f"Enabled {feature_flag} feature!")

    await message(f"!feature enable {feature_flag}")
    verify_message(f"Feature flag {feature_flag} is already enabled!")


@pytest.mark.asyncio
async def test_feature_remove(bot):
    with pytest.raises(MissingRequiredArgument):
        await message("!feature disable")

    await empty_queue()


@pytest.mark.asyncio
async def test_feature_remove_feature_flag(bot, feature_flag):
    await message(f"!player add 76561198029447509")
    verify_message("Successfully linked", contains=True)

    await message(f"!feature enable {feature_flag}")
    verify_message(f"Enabled {feature_flag} feature!")

    await message(f"!feature disable {feature_flag}")
    verify_message(f"Disabled pp_roles feature!")


@pytest.mark.asyncio
async def test_feature_remove_feature_flag_player(bot, feature_flag):
    await message(f"!feature enable {feature_flag}")
    verify_message(f"Enabled {feature_flag} feature!")

    await message(f"!feature disable {feature_flag}")
    verify_message(f"Disabled pp_roles feature!")


@pytest.mark.asyncio
async def test_feature_remove_feature_flag_already_disabled(bot, feature_flag):
    await message(f"!feature disable {feature_flag}")
    verify_message(f"Feature flag {feature_flag} is already disabled!")
