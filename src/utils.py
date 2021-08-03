import time
from functools import wraps
import math

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
    def get_pos_from_pp_weight(weight):
        position = int(round(math.log(weight, 0.965) + 1))

        return position

    @staticmethod
    def get_pp_weight_from_pos(pos):
        pp_weight = 0.965**(pos-1)

        return pp_weight
