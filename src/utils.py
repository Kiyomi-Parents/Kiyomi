import random
import time
from functools import wraps
from discord.ext import tasks

from Kiyomi import Kiyomi
import discord

from src.log import Logger


class Utils:
    @staticmethod
    def time_task(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            Logger.log(func.__name__, "<===> Starting task <===>")
            start_time = time.process_time()
            res = await func(self, *args, **kwargs)
            Logger.log(func.__name__, "Finished task in "
                                      f"{round(time.process_time() - start_time, 2)} seconds\n")

            return res

        return wrapper

    @staticmethod
    def discord_ready(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not self.uow.bot.is_ready() and not self.uow.bot.running_tests:
                Logger.log("Discord", f"Discord client not ready, skipping task {func.__name__}")
                return

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
    def class_inheritors(cls):
        subclasses = set()
        work = [cls]

        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)

        return subclasses

    @staticmethod
    def update_tasks_list(func):
        async def update_status(bot: Kiyomi):
            if bot.running_tasks:
                await bot.change_presence(activity=discord.Game(" | ".join(bot.running_tasks)))
            else:
                activity_index = random.randint(0, len(bot.activity_list)-1)
                await bot.change_presence(activity=discord.Game(bot.activity_list[activity_index]))

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if func.__doc__ not in self.uow.bot.running_tasks:
                self.uow.bot.running_tasks.append(func.__doc__)
            await update_status(self.uow.bot)
            result = await func(self, *args, **kwargs)
            if func.__doc__ in self.uow.bot.running_tasks:
                self.uow.bot.running_tasks.pop(self.uow.bot.running_tasks.index(func.__doc__))
                await update_status(self.uow.bot)
            return result

        return wrapper

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