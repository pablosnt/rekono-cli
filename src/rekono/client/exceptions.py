'''Rekono exceptions.'''

from typing import IO, Optional

import click
from click.exceptions import ClickException
from requests.models import Response


class RekonoException(ClickException):
    '''Base exception for Rekono client'''

    def __init__(self, message: str, response: Response) -> None:
        '''Exception constructor.

        Args:
            message (str): Error message.
            response (Response): Http response that causes the error.
        '''
        self.response = response
        self.message = message
        super().__init__(message)

    def show(self, file: Optional[IO] = None) -> None:
        '''Show exception message using click.

        Args:
            file (Optional[IO], optional): Defaults to None.
        '''
        click.echo(click.style(self.message, fg='red'), err=True, color=True)


class AuthenticationError(RekonoException):
    '''Authentication error during Rekono API request.'''

    def __init__(self, response: Response) -> None:
        '''Exception constructor.

        Args:
            response (Response): Http response that causes the error.
        '''
        super().__init__('Unauthorized: Invalid Rekono API token', response)


class AuthorizationError(RekonoException):
    '''Authorization error during Rekono API request.'''

    def __init__(self, response: Response) -> None:
        '''Exception constructor.

        Args:
            response (Response): Http response that causes the error.
        '''
        super().__init__('Unauthorized: User hasn\'t required permissions to perform this action', response)
