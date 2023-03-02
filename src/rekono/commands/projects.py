'''Command to perform Rekono projects operations.'''

import json
from typing import List

import click

from rekono.framework.arguments import id_mandatory_argument
from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import tags_option


class ProjectsCommand(EntityCommand):

    commands = ['get', 'create', 'update', 'delete', 'add-member', 'remove-member']     # Supported CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_entity',
        'create': 'post_entity',
        'update': 'put_entity',
        'delete': 'delete_entity',
        'add-member': 'add_member',
        'remove-member': 'remove_member'
    }
    help_messages = {
        'get': 'Retrieve entities or entity if ID is provided',
        'create': 'Create entity',
        'update': 'Update entity',
        'delete': 'Delete entity',
        'add-member': 'Add member to project',
        'remove-member': 'Remove member from project'
    }
    entity_options = [
        click.option('-n', '--name', 'name', required=True, type=str, help='Project name'),
        click.option('-d', '--description', 'description', required=True, type=str, help='Project description'),
        tags_option
    ]

    @staticmethod
    @click.command
    @click.pass_context
    @id_mandatory_argument
    @click.option('-u', '--user', 'user', required=True, type=int, help='User ID')
    def add_member(
        ctx: click.Context,
        id: int,
        user: int,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool
    ) -> None:
        ctx.invoke(
            ProjectsCommand.post, endpoint=f'/api/projects/{id}/members/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'user': user}),
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet
        )

    @staticmethod
    @click.command
    @click.pass_context
    @id_mandatory_argument
    @click.option('-u', '--user', 'user', required=True, type=int, help='User ID')
    def remove_member(
        ctx: click.Context,
        id: int,
        user: int,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool
    ) -> None:
        ctx.invoke(
            ProjectsCommand.delete, endpoint=f'/api/projects/{id}/members/{user}/',
            url=url, headers=headers, no_verify=no_verify,
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet
        )


@click.group('projects', cls=ProjectsCommand, help='Manage projects')
def projects():
    '''Manage projects.'''
