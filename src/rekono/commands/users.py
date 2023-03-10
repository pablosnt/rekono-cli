'''CLI command to manage User entities.'''

import json
from typing import List

import click

from rekono.client.enums import UserRole
from rekono.framework.arguments import id_mandatory_argument
from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option

user_role_option = click.option(                                                # Role CLI option
    '-r', '--role', 'role',
    required=False, default=UserRole.READER.value,
    type=click.Choice([t.value for t in UserRole]),
    help='User role'
)


class UsersCommand(EntityCommand):
    '''CLI command to manage User entities.'''

    commands = ['get', 'delete', 'enable', 'role', 'invite']                    # CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_entity',
        'delete': 'delete_entity',
        'role': 'update_role',
        'invite': 'invite'
    }
    help_messages = {                                                           # Help messages for each command
        'get': 'Get all users or one if ID is provided',
        'delete': 'Delete user',
        'role': 'Update user role',
        'invite': 'Invite new user'
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
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        '''Update user role.

        Args:
            ctx (click.Context): Click context.
            id (int): User ID to update.
            role (str): Role to asssin to the user.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        ctx.invoke(
            UsersCommand.put, endpoint=f'/api/users/{id}/role/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'role': role}),
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet, json_output=json_output
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
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        '''Invite new user.

        Args:
            ctx (click.Context): Click context.
            email (str): User email to send invitation to.
            role (str): Role to asssin to the user.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        ctx.invoke(
            UsersCommand.post, endpoint='/api/users/invite/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'email': email, 'role': role}),
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet, json_output=json_output
        )


@click.group('users', cls=UsersCommand, help='Manage users')
def users():
    '''Manage users.'''
