import time

from src.api.errors import *
from src.log import Logger


class Common:
    _wait_rate_limit = 60
    _wait_server_error = 5

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
            raise RateLimited(response)
        elif 400 <= response.status_code < 500:
            raise NotFound(response)
        elif 500 <= response.status_code < 600:
            raise ServerError(response)

    @staticmethod
    def request_attempt(func):
        attempt = 0
        attempting = True

        while attempting and attempt < 6:
            try:
                result = func()

                attempting = False
                return result
            except ServerError as e:
                attempt += 1
                Logger.log("Server Error", {e})
                Logger.log("Server Error", f"Waiting {Common._wait_server_error} seconds...")
                time.sleep(Common._wait_server_error)
            except RateLimited as e:
                attempt += 1
                Logger.log("Rate Limit", {e})
                Logger.log("Rate Limit", f"Waiting {Common._wait_rate_limit} seconds...")
                time.sleep(Common._wait_rate_limit)
