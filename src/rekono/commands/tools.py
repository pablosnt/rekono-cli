'''CLI command to manage Tool entities.'''

import click

from rekono.framework.commands.entity import EntityCommand


class ToolsCommand(EntityCommand):
    '''CLI command to manage Tool entities.'''

    commands = ['get']                                                          # CLI commands
    help_messages = {                                                           # Help messages for each command
        'get': 'Get all tools or one if ID is provided',
    }


@click.group('tools', cls=ToolsCommand, help='Get tools')
def tools():
    '''Get tools.'''
