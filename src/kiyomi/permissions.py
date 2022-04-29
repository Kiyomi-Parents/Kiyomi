import os
from typing import List, Callable, TypeVar

import discord
from discord import Permissions, app_commands, Interaction, Client

from src.kiyomi import OwnerOnlyCommand

T = TypeVar('T')


def _admin_guilds() -> List[discord.Object]:
    return [discord.Object(id=int(guild_id)) for guild_id in os.getenv("ADMIN_GUILDS").split(",")]


def admin_guild_list() -> List[int]:
    return [guild.id for guild in _admin_guilds()]


def admin_guild_only() -> Callable[[T], T]:
    return app_commands.guilds(*_admin_guilds())


def is_guild_staff() -> Permissions:
    raise RuntimeError("Not implemented!")


def is_guild_administrator() -> Permissions:
    raise RuntimeError("Not implemented!")


async def _bot_owners(client: Client) -> List[int]:
    app = await client.application_info()

    if app.team:
        return [member.id for member in app.team.members]
    else:
        return [app.owner.id]


def is_bot_owner() -> Callable[[T], T]:
    async def predicate(ctx: Interaction) -> bool:
        owner_ids = await _bot_owners(ctx.client)

        if ctx.user.id in owner_ids:
            return True

        raise OwnerOnlyCommand()

    return app_commands.check(predicate)


def is_bot_owner_and_admin_guild() -> Callable[[T], T]:
    return is_bot_owner()(admin_guild_only())


def is_guild_only() -> Permissions:
    raise RuntimeError("Not implemented!")
