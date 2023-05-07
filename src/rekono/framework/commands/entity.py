'''Base Rekono CLI command to make specific entity operations using API.'''

import json
from typing import Any, List, Optional, cast

import click

from rekono.framework.arguments import (id_mandatory_argument,
                                        id_optional_argument)
from rekono.framework.commands.api import ApiCommand
from rekono.framework.options import json_option


class EntityCommand(ApiCommand):
    '''Base Rekono CLI command to make specific entity operations using API.'''

    commands = ['get', 'create', 'update', 'delete']                            # CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_entity',
        'create': 'post_entity',
        'update': 'put_entity',
        'delete': 'delete_entity',
    }
    default_mapping = 'extra_post_entity'                                       # Default method if mapping not found

    @staticmethod
    @click.command
    @click.pass_context
    @id_optional_argument
    @json_option
    def get_entity(
        ctx: click.Context,
        id: Optional[int],
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ):
        '''GET request to retrieve specific entities via Rekono API.

        Args:
            ctx (click.Context): Click context.
            id (Optional[int]): Entity Id to retrieve.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        parameters = {
            'endpoint': f'/api/{cast(click.Context, ctx.parent).info_name}/',
            'url': url,
            'headers': headers,
            'no_verify': no_verify,
            'parameters': [],
            'pagination': True,
            'show_headers': show_headers,
            'only_show_status_code': only_show_status_code,
            'quiet': quiet,
            'json_output': json_output
        }
        if id:
            parameters.update({
                'endpoint': f'/api/{cast(click.Context, ctx.parent).info_name}/{id}/',
                'pagination': False
            })
        ctx.invoke(EntityCommand.get, **parameters)

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
        ctx.invoke(
            EntityCommand.post, endpoint=f'/api/{cast(click.Context, ctx.parent).info_name}/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps(kwargs),
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet,
            json_output=json_output
        )

    @staticmethod
    @click.command
    @click.pass_context
    @id_mandatory_argument
    @json_option
    def put_entity(
        ctx: click.Context,
        id: int,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str,
        **kwargs: Any
    ) -> None:
        '''PUT request to update specific entity via Rekono API.

        Args:
            ctx (click.Context): Click context.
            id (int): Entity Id to updae.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
            kwargs (Any): Variable fields that will be sent as body.
        '''
        ctx.invoke(
            EntityCommand.put, endpoint=f'/api/{cast(click.Context, ctx.parent).info_name}/{id}/',
            url=url, headers=headers, no_verify=no_verify, body=json.dumps(kwargs),
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet,
            json_output=json_output
        )

    @staticmethod
    @click.command
    @click.pass_context
    @id_mandatory_argument
    def delete_entity(
        ctx: click.Context,
        id: int,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool
    ):
        '''DELETE request to remove specific entity via Rekono API.

        Args:
            ctx (click.Context): Click context.
            id (int): Entity Id to remove.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
        '''
        ctx.invoke(
            EntityCommand.delete, endpoint=f'/api/{cast(click.Context, ctx.parent).info_name}/{id}/',
            url=url, headers=headers, no_verify=no_verify,
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet
        )

    @staticmethod
    @click.command
    @click.pass_context
    @id_mandatory_argument
    def extra_post_entity(
        ctx: click.Context,
        id: int,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool
    ) -> None:
        '''POST request to make some operation against specific entity via Rekono API.

        Args:
            ctx (click.Context): Click context.
            id (int): Entity Id to updae.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
        '''
        ctx.invoke(
            EntityCommand.post, endpoint=f'/api/{cast(click.Context, ctx.parent).info_name}/{id}/{ctx.info_name}/',
            url=url, headers=headers, no_verify=no_verify, body=None,
            show_headers=show_headers, only_show_status_code=only_show_status_code, quiet=quiet,
            json_output=None
        )
