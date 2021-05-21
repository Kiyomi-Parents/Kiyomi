class APIException(Exception):
    def __init__(self, response, message=None):
        self.response = response

        if message is not None:
            self.message = message
        else:
            self.message = f"Got HTTP status code {response.status_code} for {response.url}"

    def __str__(self):
        return self.message


class NotFound(APIException):
    pass


class RateLimited(APIException):
    pass


class ServerError(APIException):
    pass
