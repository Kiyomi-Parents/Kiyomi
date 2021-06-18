import pytest
from discord.ext.commands import MissingRequiredArgument
from discord.ext.test import message, verify, empty_queue


def pytest_generate_tests(metafunc):
    if "feature_flag" in metafunc.fixturenames:
        metafunc.parametrize("feature_flag", ["pp_roles"], indirect=True)


@pytest.fixture(scope="module")
def feature_flag(request):
    return request.param


@pytest.mark.asyncio
async def test_feature():
    await message("!feature")
    assert verify() \
        .message() \
        .contains() \
        .content("Type !help command for more info on a command.")


@pytest.mark.asyncio
async def test_feature_enable():
    with pytest.raises(MissingRequiredArgument):
        await message("!feature enable")

    await empty_queue()


@pytest.mark.asyncio
async def test_feature_enable_feature_flag(feature_flag):
    await message(f"!feature enable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Enabled {feature_flag} feature!")


@pytest.mark.asyncio
async def test_feature_enable_feature_flag_player(feature_flag):
    await message(f"!player add 76561198029447509")
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message(f"!feature enable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Enabled {feature_flag} feature!")


@pytest.mark.asyncio
async def test_feature_enable_feature_flag_already_enabled(feature_flag):
    await message(f"!feature enable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Enabled {feature_flag} feature!")

    await message(f"!feature enable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Feature flag {feature_flag} is already enabled!")


@pytest.mark.asyncio
async def test_feature_remove():
    with pytest.raises(MissingRequiredArgument):
        await message("!feature disable")

    await empty_queue()


@pytest.mark.asyncio
async def test_feature_remove_feature_flag(feature_flag):
    await message("!player add 76561198029447509")
    assert verify() \
        .message() \
        .contains() \
        .content("Successfully linked")

    await message(f"!feature enable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Enabled {feature_flag} feature!")

    await message(f"!feature disable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Disabled {feature_flag} feature!")


@pytest.mark.asyncio
async def test_feature_remove_feature_flag_player(feature_flag):
    await message(f"!feature enable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Enabled {feature_flag} feature!")

    await message(f"!feature disable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Disabled {feature_flag} feature!")


@pytest.mark.asyncio
async def test_feature_remove_feature_flag_already_disabled(feature_flag):
    await message(f"!feature disable {feature_flag}")
    assert verify() \
        .message() \
        .content(f"Feature flag {feature_flag} is already disabled!")
