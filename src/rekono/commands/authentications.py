import click

from rekono.client.enums import AuthenticationType
from rekono.framework.commands.entity import EntityCommand


class AuthenticationsCommand(EntityCommand):
    
    entity_options = [
        click.option('-p', '--target-port', 'target_port', required=True, type=int, help='Related target port ID'),
        click.option('-n', '--name', 'name', required=True, type=str, help='Authentication name'),
        click.option('-c', '--credential', 'credential', required=True, type=str, help='Authentication secret value'),
        click.option(
            '-t', '--type', 'auth_type',
            required=True, default=AuthenticationType.BASIC,
            type=click.Choice([t.value for t in AuthenticationType]),
            help='Authentication type'
        )
    ]


@click.group('authentications', cls=AuthenticationsCommand, help='Manage authentication with targets')
def authentications():
    '''Manage authentication with targets.'''
