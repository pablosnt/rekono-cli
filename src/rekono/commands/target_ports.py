import click

from rekono.framework.commands.entity import EntityCommand


class TargetPortsCommand(EntityCommand):

    commands = ['get', 'create', 'delete']                                      # Supported CLI commands
    entity_options = [
        click.option('-t', '--target', 'target', required=True, type=int, help='Target ID'),
        click.option('-p', '--port', 'port', required=True, type=int, help='Port number')
    ]


@click.group('target-ports', cls=TargetPortsCommand, help='Manage target ports')
def target_ports():
    '''Manage target ports.'''
