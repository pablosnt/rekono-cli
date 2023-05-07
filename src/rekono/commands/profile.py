'''CLI command to manage user profile.'''

import json
from typing import List

import click

from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option


class ProfileCommand(EntityCommand):
    '''CLI command to manage user profile.'''

    commands = ['get', 'telegram']                                              # CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_profile',
        'telegram': 'link_telegram_bot'
    }
    help_messages = {                                                           # Help messages for each command
        'get': 'Get current user profile',
        'telegram': 'Link Telegram bot to current user'
    }

    @staticmethod
    @click.command
    @click.pass_context
    @json_option
    def get_profile(
        ctx: click.Context,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ) -> None:
        '''Get current user profile.

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
            ProfileCommand.get, endpoint='/api/profile/',
            url=url, headers=headers, no_verify=no_verify, parameters=[], pagination=False,
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet, json_output=json_output
        )

    @staticmethod
    @click.command
    @click.pass_context
    @click.option('-t', '--token', 'token', required=True, type=str, help='Token provided by Telegram bot')
    def link_telegram_bot(
        ctx: click.Context,
        token: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool
    ) -> None:
        '''Link user account to Telegram chat.

        Args:
            ctx (click.Context): Click context.
            token (str): Temporal token provided by Rekono bot.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
        '''
        ctx.invoke(
            ProfileCommand.post, endpoint='/api/profile/telegram-token/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'otp': token}),
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet, json_output=None
        )


@click.group('profile', cls=ProfileCommand, help='Manage user profile')
def profile():
    '''Manage user profile.'''
