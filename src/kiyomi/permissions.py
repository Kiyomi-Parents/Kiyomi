import os
from typing import Callable

from discord import SlashCommand
from discord.commands import permissions


def is_guild_staff():
    return permissions.has_permissions(manage_messages=True)


def is_guild_administrator():
    return permissions.has_permissions(administrator=True)


def is_bot_owner():
    def inner(command: Callable):
        if isinstance(command, SlashCommand):
            command.guild_ids = os.getenv("ADMIN_GUILDS").split(",")
        return command

    return inner


def is_guild_only():
    return permissions.guild_only()
