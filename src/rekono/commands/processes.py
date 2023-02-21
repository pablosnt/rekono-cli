import click

from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import tags_option


class ProcessesCommand(EntityCommand):

    entity_options = [
        click.option('-n', '--name', 'name', required=True, type=str, help='Process name'),
        click.option('-d', '--description', 'description', required=True, type=str, help='Process description'),
        tags_option
    ]


@click.group('processes', cls=ProcessesCommand, help='Manage processes')
def processes():
    '''Manage processes.'''
