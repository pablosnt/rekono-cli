'''Rekono exceptions.'''

from requests.models import Response


class AuthenticationError(Exception):
    '''Authentication error during authentication attempt.'''

    def __init__(self, message: str, response: Response) -> None:
        '''Exception constructor.

        Args:
            message (str): Error message.
            response (Response): Http response that causes the error.
        '''
        self.response = response
        self.message = message
        super().__init__(message)
