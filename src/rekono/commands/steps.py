import click

from rekono.framework.commands.entity import EntityCommand


class StepsCommand(EntityCommand):

    entity_options = [
        click.option('-p', '--process', 'process', required=True, type=int, help='Process ID'),
        click.option('-t', '--tool', 'tool_id', required=True, type=int, help='Tool ID'),
        click.option('-c', '--configuration', 'configuration_id', required=True, type=int, help='Configuration ID'),
        click.option('--priority', 'priority', required=False, default=1, type=int, help='Step priority within process')
    ]


@click.group('steps', cls=StepsCommand, help='Manage steps')
def steps():
    '''Manage steps.'''
