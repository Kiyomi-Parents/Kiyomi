class APIException(Exception):
    def __init__(self, response, message=None):
        self.response = response

        if message is not None:
            self.message = message
        else:
            self.message = f"Got HTTP status code {response.status_code} for {response.url}"

    def __str__(self):
        return self.message


class NotFoundException(APIException):
    pass


class RateLimitedException(APIException):
    pass


class ServerErrorException(APIException):
    pass
