import json
from typing import List

import click

from rekono.client.enums import UserRole
from rekono.framework.arguments import id_mandatory_argument
from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option

user_role_option = click.option(
    '-r', '--role', 'role',
    required=False, default=UserRole.READER.value,
    type=click.Choice([t.value for t in UserRole]),
    help='User role'
)


class UsersCommand(EntityCommand):
    '''Base Rekono CLI command for finding entities.'''

    commands = ['get', 'delete', 'enable', 'role', 'invite']                    # Supported CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_entity',
        'delete': 'delete_entity',
        'role': 'update_role',
        'invite': 'invite'
    }

    @staticmethod
    @click.command
    @click.pass_context
    @id_mandatory_argument
    @user_role_option
    @json_option
    def update_role(
        ctx: click.Context,
        id: int,
        role: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        ctx.invoke(
            UsersCommand.put, endpoint=f'/api/users/{id}/role/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'role': role}),
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet, json_output=json_output
        )

    @staticmethod
    @click.command
    @click.pass_context
    @click.option('-e', '--email', 'email', required=True, type=str, help='User email to send invitation')
    @user_role_option
    @json_option
    def invite(
        ctx: click.Context,
        email: str,
        role: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        ctx.invoke(
            UsersCommand.post, endpoint='/api/users/invite/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'email': email, 'role': role}),
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet, json_output=json_output
        )


@click.group('users', cls=UsersCommand, help='Manage users')
def users():
    '''Manage users.'''