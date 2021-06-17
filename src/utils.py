import time
from functools import wraps

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
