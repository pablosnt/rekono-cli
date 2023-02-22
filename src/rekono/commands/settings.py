from typing import List

import click

from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option


class SettingsCommand(EntityCommand):

    commands = ['get']
    commands_mapping = {
        'get': 'get_settings'
    }
    help_messages = {
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
        just_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        ctx.invoke(
            SettingsCommand.get, endpoint='/api/system/1/',
            url=url, headers=headers, no_verify=no_verify, parameters=[], all_pages=False,
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet, json_output=json_output
        )


@click.group('settings', cls=SettingsCommand, help='Get system settings')
def settings():
    '''Get system settings.'''