import os
from typing import List, Dict

from discord import CommandPermission


def admin_guild_only() -> Dict[str, List[int]]:
    admin_guilds = [int(guild_id) for guild_id in os.getenv("ADMIN_GUILDS").split(",")]

    return {"guild_ids": admin_guilds}


def is_guild_staff() -> List[CommandPermission]:
    raise RuntimeError("Not implemented!")


def is_guild_administrator() -> List[CommandPermission]:
    raise RuntimeError("Not implemented!")


def is_bot_owner() -> Dict[str, List[CommandPermission]]:
    permissions = [CommandPermission("owner", 2, True, None)]

    return {"permissions": permissions}


def is_bot_owner_and_admin_guild() -> Dict[str, List[any]]:
    return {
        **is_bot_owner(),
        **admin_guild_only()
    }


def is_guild_only() -> List[CommandPermission]:
    raise RuntimeError("Not implemented!")
