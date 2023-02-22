from typing import Any, List

import click

from rekono.client.enums import WordlistType
from rekono.framework.commands.entity import EntityCommand


class WordlistsCommand(EntityCommand):

    entity_options = [
        click.option('-n', '--name', 'name', required=True, type=str, help='Wordlist name'),
        click.option(
            '-t', '--type', 'type',
            required=True, default=WordlistType.ENDPOINT,
            type=click.Choice([t.value for t in WordlistType]),
            help='Wordlist name'
        )
    ]
    
    @staticmethod
    @click.command
    @click.pass_context
    @click.option('-f', '--file', 'file', required=True, type=click.File('rb'), help='Wordlists file')
    @json_option
    def post_entity(
        ctx: click.Context,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool,
        json_output: str,
        **kwargs: Any
    ) -> None:
        super().post_entity(
            ctx, url, headers, no_verify, show_headers, just_show_status_code, quiet, json_output, **kwargs
        )


@click.group('wordlists', cls=WordlistsCommand, help='Manage wordlists')
def wordlists():
    '''Manage wordlists.'''
