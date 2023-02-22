import json
from typing import Any, List

import click

from rekono.client.enums import WordlistType
from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option


class WordlistsCommand(EntityCommand):

    entity_options = [
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
        filepath: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool,
        json_output: str,
        **kwargs: Any
    ) -> None:
        ctx.invoke(
            WordlistsCommand.post, endpoint='/api/wordlists/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps(kwargs),
            show_headers=show_headers, just_show_status_code=just_show_status_code,
            quiet=quiet, json_output=json_output, filepath=filepath
        )


@click.group('wordlists', cls=WordlistsCommand, help='Manage wordlists')
def wordlists():
    '''Manage wordlists.'''
