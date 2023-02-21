'''Command to perform Rekono tools operations.'''

import click

from rekono.framework.commands.entity import EntityCommand


class ToolsCommand(EntityCommand):

    commands = ['get']


@click.group('tools', cls=ToolsCommand, help='Get tools')
def tools():
    '''Get tools.'''


@click.group('configurations', cls=ToolsCommand, help='Get configurations')
def configurations():
    '''Get configurations.'''
