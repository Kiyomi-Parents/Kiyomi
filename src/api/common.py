import time

from src.api.errors import *
from src.log import Logger

wait_rate_limit = 60
wait_server_error = 5


class Common:

    @staticmethod
    def request(method, *args, **kwargs):
        def attempt():
            response = method(*args, **kwargs)
            Common.verify_response(response)
            return response

        return Common.request_attempt(attempt)

    @staticmethod
    def verify_response(response):
        if response.status_code == 429:
            raise RateLimitedException(response)
        elif 400 <= response.status_code < 500:
            raise NotFoundException(response)
        elif 500 <= response.status_code < 600:
            raise ServerErrorException(response)

    @staticmethod
    def request_attempt(func):
        attempt = 0
        attempting = True
        last_exception = None

        while attempting and attempt < 6:
            try:
                result = func()

                attempting = False
                return result
            except ServerErrorException as e:
                attempt += 1
                Logger.log("Server Error", str(e))
                Logger.log("Server Error", f"Waiting {wait_server_error} seconds...")
                last_exception = e
                time.sleep(wait_server_error)
            except RateLimitedException as e:
                attempt += 1
                Logger.log("Rate Limit", str(e))
                Logger.log("Rate Limit", f"Waiting {wait_rate_limit} seconds...")
                last_exception = e
                time.sleep(wait_rate_limit)

        raise last_exception
