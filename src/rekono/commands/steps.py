'''CLI command to manage Step entities.'''

import click

from rekono.framework.commands.entity import EntityCommand


class StepsCommand(EntityCommand):
    '''CLI command to manage Step entities.'''

    help_messages = {                                                           # Help messages for each command
        'get': 'Get all steps or one if ID is provided',
        'create': 'Create step',
        'update': 'Update step',
        'delete': 'Delete step',
    }
    entity_options = [                                                          # Specific options for post and put
        click.option('-p', '--process', 'process', required=True, type=int, help='Process ID'),
        click.option('-t', '--tool', 'tool_id', required=True, type=int, help='Tool ID'),
        click.option('-c', '--configuration', 'configuration_id', required=True, type=int, help='Configuration ID'),
        click.option('--priority', 'priority', required=False, default=1, type=int, help='Step priority within process')
    ]


@click.group('steps', cls=StepsCommand, help='Manage steps')
def steps():
    '''Manage steps.'''
