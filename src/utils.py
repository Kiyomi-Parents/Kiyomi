import time
from functools import wraps, partial
from typing import Callable, Coroutine

from asyncio import to_thread

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
    def on_thread(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await to_thread(func, *args, **kwargs)

        return wrapper
