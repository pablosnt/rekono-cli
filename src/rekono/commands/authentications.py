'''CLI command to manage Authentication entities.'''

import click

from rekono.client.enums import AuthenticationType
from rekono.framework.commands.entity import EntityCommand


class AuthenticationsCommand(EntityCommand):
    '''CLI command to manage Authentication entities.'''

    help_messages = {                                                           # Help messages for each command
        'get': 'Get all wordlists or one if ID is provided',
        'create': 'Create wordlist',
        'update': 'Update wordlist',
        'delete': 'Delete wordlist',
    }
    entity_options = [                                                          # Specific options for post and put
        click.option('-p', '--target-port', 'target_port', required=True, type=int, help='Related target port ID'),
        click.option('-n', '--name', 'name', required=True, type=str, help='Authentication name'),
        click.option('-c', '--credential', 'credential', required=True, type=str, help='Authentication secret value'),
        click.option(
            '-t', '--type', 'auth_type',
            required=False, default=AuthenticationType.BASIC.value,
            type=click.Choice([t.value for t in AuthenticationType]),
            help='Authentication type'
        )
    ]


@click.group('authentications', cls=AuthenticationsCommand, help='Manage target authentications')
def authentications():
    '''Manage target authentications.'''
