from requests.models import Response


class AuthenticationError(Exception):
    
    def __init__(self, message: str, response: Response) -> None:
        self.response = response
        self.message = message
        super().__init__(message)
