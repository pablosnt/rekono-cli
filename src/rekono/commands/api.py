'''Command to perform standard Rekono API requests.'''

import click

from rekono.framework.commands.api import ApiCommand


@click.group('api', cls=ApiCommand, help='Perform Rekono API requests')
def api():
    '''Perform Rekono API requests.'''
