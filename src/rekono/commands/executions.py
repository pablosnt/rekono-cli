'''Command to perform Rekono configurations operations.'''

import click

from rekono.framework.commands.entity import EntityCommand


class ExecutionsCommand(EntityCommand):

    commands = ['get']


@click.group('executions', cls=ExecutionsCommand, help='Get executions')
def executions():
    '''Get executions.'''
