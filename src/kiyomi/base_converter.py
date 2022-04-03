from abc import ABC

from discord.ext import commands


class BaseConverter(commands.Converter, ABC):
    pass