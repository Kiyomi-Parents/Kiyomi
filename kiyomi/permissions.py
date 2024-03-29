from typing import List, Callable, TypeVar

import discord
from discord import Permissions, app_commands, Interaction, Client

from kiyomi import OwnerOnlyCommand, Config

T = TypeVar("T")


def _admin_guilds() -> List[discord.Object]:
    admin_guilds = Config.get().Discord.Guilds.Admin
    if admin_guilds is not None and len(admin_guilds) > 0:
        return [discord.Object(id=int(guild_id)) for guild_id in admin_guilds]
    return []


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
