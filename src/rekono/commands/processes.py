'''CLI command to manage Process entities.'''

import click

from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import tags_option


class ProcessesCommand(EntityCommand):
    '''CLI command to manage Process entities.'''

    help_messages = {                                                           # Help messages for each command
        'get': 'Get all processes or one if ID is provided',
        'create': 'Create process',
        'update': 'Update process',
        'delete': 'Delete process'
    }
    entity_options = [                                                          # Specific options for post and put
        click.option('-n', '--name', 'name', required=True, type=str, help='Process name'),
        click.option('-d', '--description', 'description', required=True, type=str, help='Process description'),
        tags_option
    ]


@click.group('processes', cls=ProcessesCommand, help='Manage processes')
def processes():
    '''Manage processes.'''
