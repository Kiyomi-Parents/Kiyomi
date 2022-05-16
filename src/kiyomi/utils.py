import asyncio
from datetime import datetime
from functools import wraps
from typing import TypeVar, Type, List, Any, Dict

import discord
import timeago
from discord.ext import tasks

from src.kiyomi.timer import Timer
from src.log import Logger

TClass = TypeVar('TClass')


class Utils:
    @staticmethod
    def time_task(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            Logger.log(func.__name__, "<===> Starting task <===>")

            start_time = datetime.now()
            res = await func(self, *args, **kwargs)
            end_time = datetime.now()

            Logger.log(
                    func.__name__, f"Finished task in {timeago.format(start_time, end_time)}\n"
            )

            return res

        return wrapper

    @staticmethod
    def discord_ready(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not self.bot.is_ready() and not self.bot.running_tests:
                await self.bot.wait_until_ready()
                await asyncio.sleep(1)

            return await func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def update_class(old_class, new_class):
        if type(new_class) is not type(old_class):
            raise TypeError(f"Failed to update class. {type(new_class)} is not of type {type(old_class)}")

        for var in old_class.__dict__.keys():
            # Ignore private variables
            if var.startswith("_"):
                continue

            if var in new_class.__dict__.keys():
                if getattr(new_class, var) is not None:
                    setattr(old_class, var, getattr(new_class, var))

    @staticmethod
    def updated_class_fields(old_class, new_class) -> Dict:
        if type(new_class) is not type(old_class):
            raise TypeError(f"Failed to update class. {type(new_class)} is not of type {type(old_class)}")

        updated_values = {}
        for var in old_class.__dict__.keys():
            # Ignore private variables
            if var.startswith("_"):
                continue

            if var in new_class.__dict__.keys():
                old_attr = getattr(old_class, var)
                new_attr = getattr(new_class, var)

                if new_attr is not None and new_attr is not old_attr:
                    updated_values[var] = new_attr

        return updated_values

    @staticmethod
    def get_class_fields(cls) -> Dict:
        fields = {}

        for var in cls.__dict__.keys():
            # Ignore private variables
            if var.startswith("_"):
                continue

            fields[var] = getattr(cls, var)

        return fields

    @staticmethod
    def class_inheritors(cls: Type[TClass]) -> List[Type[TClass]]:
        subclasses = set()
        work = [cls]

        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)

        return list(subclasses)

    @staticmethod
    def combine_decorators(*decs):
        def deco(f):
            for dec in reversed(decs):
                f = dec(f)
            return f

        return deco

    @staticmethod
    def sub_tasks_decorator(func):
        @Utils.combine_decorators(Utils.time_task, Utils.discord_ready)
        @wraps(func)
        def wrapper():
            return func()

        return wrapper

    @staticmethod
    def tasks_decorator(seconds=0, minutes=0, hours=0, count=None, reconnect=True, loop=None):
        def decorator(func):
            @tasks.loop(seconds=seconds, minutes=minutes, hours=hours, count=count, reconnect=reconnect, loop=loop)
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                return await func(self, *args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def text_to_file(text: str, file_name: str) -> discord.File:
        with open(f"./tmp/{file_name}", "w") as file:
            file.write(text)

        return discord.File(fp=f"./tmp/{file_name}", filename=file_name)

    @staticmethod
    def debounce(wait_time):
        """
        Decorator that will debounce a function so that it is called after wait_time seconds
        If it is called multiple times, will wait for the last call to be debounced and run only this one.
        """

        def decorator(function):
            async def debounced(*args, **kwargs):
                async def call_function():
                    debounced._timer = None
                    return await function(*args, **kwargs)

                # if we already have a call to the function currently waiting to be executed, reset the timer
                if debounced._timer is not None:
                    debounced._timer.cancel()

                # after wait_time, call the function provided to the decorator with its arguments
                debounced._timer = Timer(wait_time, call_function)

            debounced._timer = None
            return debounced

        return decorator

    @staticmethod
    def limit_list(items: List[Any], limit: int) -> List[Any]:
        if len(items) > limit:
            return items[:limit]

        return items
