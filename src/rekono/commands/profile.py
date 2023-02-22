from typing import List

import click

from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option
import json


class ProfileCommand(EntityCommand):

    commands = ['get']
    commands_mapping = {
        'get': 'get_profile',
        'telegram': 'link_telegram_bot'
    }
    help_messages = {
        'get': 'Get current user profile',
        'telegram': 'Link Telegram bot to current user'
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
            ProfileCommand.get, endpoint='/api/profile/',
            url=url, headers=headers, no_verify=no_verify, parameters=[], all_pages=False,
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet, json_output=json_output
        )

    @staticmethod
    @click.command
    @click.pass_context
    @click.option('-t', '--token', 'token', required=True, type=str, help='Token provided by Telegram bot'),
    def link_telegram_bot(
        ctx: click.Context,
        token: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool
    ) -> None:
        ctx.invoke(
            ProfileCommand.post, endpoint='/api/profile/telegram-token/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps({'otp': token}),
            show_headers=show_headers, just_show_status_code=just_show_status_code, quiet=quiet, json_output=None
        )


@click.group('profile', cls=ProfileCommand, help='Get user profile')
def profile():
    '''Get user profile.'''
