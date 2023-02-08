'''Command to perform Rekono API requests.'''

import click

from rekono.framework.commands import RekonoApiCommand


@click.group('api', cls=RekonoApiCommand, help='Perform Rekono API requests')
def api():
    '''Perform Rekono API requests.'''
