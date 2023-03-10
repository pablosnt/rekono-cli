'''CLI command to manage Task entities.'''

import json
from typing import Any, List

import click

from rekono.client.enums import IntensityRank, TimeUnit
from rekono.framework.commands.entity import EntityCommand
from rekono.framework.options import json_option


class TasksCommand(EntityCommand):
    '''CLI command to manage Task entities.'''

    commands = ['get', 'create', 'cancel', 'repeat']                            # CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_entity',
        'create': 'post_entity',
        'cancel': 'delete_entity'
    }
    help_messages = {                                                           # Help messages for each command
        'get': 'Get all tasks or one if ID is provided',
        'create': 'Create task',
        'cancel': 'Cancel task execution',
    }
    entity_options = [                                                          # Specific options for post and put
        click.option('-t', '--target', 'target_id', required=True, type=int, help='Process ID'),
        click.option('-p', '--process', 'process_id', required=False, default=None, type=int, help='Process ID'),
        click.option('--tool', 'tool_id', required=False, default=None, type=int, help='Tool ID'),
        click.option(
            '-c', '--configuration', 'configuration_id',
            required=False, default=None,
            type=int, help='Configuration ID'
        ),
        click.option(
            '-i', '--intensity', 'intensity_rank',
            required=False, default=IntensityRank.NORMAL.value,
            type=click.Choice([t.value for t in IntensityRank]),
            help='Intensity rank'
        ),
        click.option(
            '-sat', '--scheduled-at', 'scheduled_at',
            required=False, type=click.DateTime(formats=['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']),
            help='Exactly time to scheduled task at'
        ),
        click.option(
            '-sin', '--scheduled-in', 'scheduled_in',
            required=False, type=int, help='Schedule task to some time later'
        ),
        click.option(
            '-stu', '--scheduled-time-unit', 'scheduled_time_unit',
            required=False, type=click.Choice([t.value for t in TimeUnit]),
            help='Time unit to apply in scheduling'
        ),
        click.option(
            '-rin', '--repeat-in', 'repeat_in',
            required=False, type=int, help='Repeat task periodically after some time'
        ),
        click.option(
            '-rtu', '--repeat-time-unit', 'repeat_time_unit',
            required=False, type=click.Choice([t.value for t in TimeUnit]),
            help='Time unit to apply in repeating'
        ),
        click.option('-w', '--wordlist', 'wordlists', multiple=True, required=False, type=int, help='Wordlist ID')
    ]

    @staticmethod
    @click.command
    @click.pass_context
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
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
            kwargs (Any): Variable fields that will be sent as body
        '''
        for no_null_field in ['process_id', 'tool_id', 'configuration_id']:
            if no_null_field in kwargs and not kwargs.get(no_null_field):       # Empty value
                kwargs.pop(no_null_field)                                       # Remove empty values from body data
        # Set scheduled_at field as ISO format
        kwargs['scheduled_at'] = kwargs['scheduled_at'].astimezone().isoformat() if kwargs.get('scheduled_at') else None
        ctx.invoke(
            TasksCommand.post, endpoint='/api/tasks/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps(kwargs),
            show_headers=show_headers, only_show_status_code=only_show_status_code,
            quiet=quiet, json_output=json_output
        )


@click.group('tasks', cls=TasksCommand, help='Manage tasks')
def tasks():
    '''Manage tasks.'''
