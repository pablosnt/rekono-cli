'''CLI command to manage system settings.'''

from typing import List

import click

from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option


class SettingsCommand(EntityCommand):
    '''CLI command to manage system settings.'''

    commands = ['get']                                                          # CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_settings'
    }
    help_messages = {                                                           # Help messages for each command
        'get': 'Get system settings'
    }

    @staticmethod
    @click.command
    @click.pass_context
    @json_option
    def get_settings(
        ctx: click.Context,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        '''Get current system settings.

        Args:
            ctx (click.Context): Click context.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        ctx.invoke(
            SettingsCommand.get, endpoint='/api/system/1/',
            url=url, headers=headers, no_verify=no_verify, parameters=[], pagination=False,
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet, json_output=json_output
        )


@click.group('settings', cls=SettingsCommand, help='Get system settings')
def settings():
    '''Get system settings.'''
