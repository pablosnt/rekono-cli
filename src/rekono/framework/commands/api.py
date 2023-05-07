'''Base Rekono CLI command to make API requests.'''

from typing import List

import click

from rekono.framework.arguments import endpoint_argument
from rekono.framework.commands.command import RekonoCliCommand
from rekono.framework.options import (all_pages_option, body_option,
                                      file_option, headers_option, json_option,
                                      no_verify_option, parameters_option,
                                      quiet_option, show_headers_option,
                                      show_status_code_option, url_option)


class ApiCommand(RekonoCliCommand):
    '''Base Rekono CLI command to make API requests.'''

    commands = ['get', 'post', 'put', 'delete']                                 # List of supported commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get',
        'post': 'post',
        'put': 'put',
        'delete': 'delete'
    }
    help_messages = {                                                           # Help messages for each command
        'get': 'GET request to Rekono API',
        'post': 'POST request to Rekono API',
        'put': 'PUT request to Rekono API',
        'delete': 'DELETE request to Rekono API'
    }
    api_options = [url_option, headers_option, no_verify_option]                # API options for all commands
    display_options = [show_headers_option, show_status_code_option, quiet_option]  # Display options for all commands

    @staticmethod
    @click.command
    @endpoint_argument
    @parameters_option
    @all_pages_option
    @json_option
    def get(
        endpoint: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        parameters: List[str],
        pagination: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ):
        '''GET request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            parameters (List[str]): HTTP query parameters to send in key=value format.
            no_verify (bool): Disable TLS validation.
            pagination (bool): Enable iteration over all API pages.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        client = ApiCommand._rekono_factory(url, no_verify, headers)
        response_or_responses = client.get(
            ApiCommand._get_endpoint(endpoint),
            parameters=ApiCommand._parse_key_value_params(parameters),
            pagination=pagination
        )
        responses = response_or_responses if isinstance(response_or_responses, list) else [response_or_responses]
        ApiCommand._display_responses(responses, show_headers, only_show_status_code, quiet)
        ApiCommand._save_output(responses, json_output)

    @staticmethod
    @click.command
    @endpoint_argument
    @body_option
    @file_option
    @json_option
    def post(
        endpoint: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        body: str,
        filepath: str,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ):
        '''POST request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            body (str): HTTP body to send in JSON format.
            filepath (click.Path): File to upload.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        client = ApiCommand._rekono_factory(url, no_verify, headers)
        response = client.post(ApiCommand._get_endpoint(endpoint), ApiCommand._get_body(body), filepath)
        ApiCommand._display_responses([response], show_headers, only_show_status_code, quiet)
        ApiCommand._save_output([response], json_output)

    @staticmethod
    @click.command
    @endpoint_argument
    @body_option
    @json_option
    def put(
        endpoint: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        body: str,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool,
        json_output: str
    ):
        '''PUT request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            body (str): HTTP body to send in JSON format.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        client = ApiCommand._rekono_factory(url, no_verify, headers)
        response = client.put(ApiCommand._get_endpoint(endpoint), ApiCommand._get_body(body))
        ApiCommand._display_responses([response], show_headers, only_show_status_code, quiet)
        ApiCommand._save_output([response], json_output)

    @staticmethod
    @click.command
    @endpoint_argument
    def delete(
        endpoint: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool
    ):
        '''DELETE request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
        '''
        client = ApiCommand._rekono_factory(url, no_verify, headers)
        response = client.delete(ApiCommand._get_endpoint(endpoint))
        ApiCommand._display_responses([response], show_headers, only_show_status_code, quiet)
