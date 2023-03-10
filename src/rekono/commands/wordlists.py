'''CLI command to manage Wordlist entities.'''

import json
from typing import Any, List

import click

from rekono.client.enums import WordlistType
from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option


class WordlistsCommand(EntityCommand):
    '''CLI command to manage Wordlist entities.'''

    help_messages = {                                                           # Help messages for each command
        'get': 'Get all wordlists or one if ID is provided',
        'create': 'Create wordlist',
        'update': 'Update wordlist',
        'delete': 'Delete wordlist',
    }
    entity_options = [                                                          # Specific options for post and put
        click.option('-n', '--name', 'name', required=True, type=str, help='Wordlist name'),
        click.option(
            '-t', '--type', 'type',
            required=False, default=WordlistType.ENDPOINT.value,
            type=click.Choice([t.value for t in WordlistType]),
            help='Wordlist name'
        )
    ]

    @staticmethod
    @click.command
    @click.pass_context
    @click.option('-f', '--file', 'filepath', required=True, type=click.Path(exists=True), help='Wordlists file')
    @json_option
    def post_entity(
        ctx: click.Context,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str,
        **kwargs: Any
    ) -> None:
        '''POST request to create specific entity via Rekono API.

        Args:
            ctx (click.Context): Click context.
            filepath (str): Filepath to upload as wordlist file.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
            kwargs (Any): Variable fields that will be sent as body
        '''
        filepath = kwargs.pop('filepath')
        ctx.invoke(
            WordlistsCommand.post, endpoint='/api/wordlists/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps(kwargs),
            show_headers=show_headers, only_show_status_code=only_show_status_code,
            quiet=quiet, json_output=json_output, filepath=filepath
        )


@click.group('wordlists', cls=WordlistsCommand, help='Manage wordlists')
def wordlists():
    '''Manage wordlists.'''
