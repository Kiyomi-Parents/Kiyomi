import pytest


@pytest.fixture
async def text_channel_factory(guild):
    class Factory:
        @staticmethod
        async def make(override_guild=None):
            if override_guild is not None:
                return await override_guild.create_text_channel(f"Channel_{len(override_guild.text_channels)}")

            return await guild.create_text_channel(f"Channel_{len(guild.text_channels)}")

    return Factory()


@pytest.fixture
async def text_channel(text_channel_factory):
    return await text_channel_factory.make()
