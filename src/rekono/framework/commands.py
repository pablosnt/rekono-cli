'''Definition of base features for CLI commands.'''

import json
import os
import sys
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import click
import requests
from requests.models import Response

from rekono.client.api import Rekono
from rekono.client.exceptions import AuthenticationError
from rekono.framework.arguments import endpoint_argument
from rekono.framework.options import (all_pages_option, body_option,
                                      headers_option, json_option,
                                      no_verify_option, parameters_option,
                                      quiet_option, show_headers_option,
                                      status_code_option, url_option)


class RekonoApiCommand(click.MultiCommand):
    '''Base Rekono CLI command.'''

    api_token_env = 'REKONO_TOKEN'                                              # Environment variable to set API token
    commands = ['get', 'post', 'put', 'delete']                                 # List of CLI commands supported

    def list_commands(self, ctx: click.Context) -> List[str]:
        '''Return list of CLI commands.

        Args:
            ctx (click.Context): Click context.

        Returns:
            List[str]: List of CLI commands.
        '''
        return self.commands

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        '''Get CLI command by name.

        Args:
            ctx (click.Context): Click context.
            cmd_name (str): Command name.

        Returns:
            Optional[click.Command]: Click command.
        '''
        return getattr(self, cmd_name) if hasattr(self, cmd_name) else None

    @staticmethod
    def _get_url(url: str) -> str:
        '''Get valid Rekono base URL from the user provided value.

        Args:
            url (str): User provided URL.

        Returns:
            str: Valid Rekono base URL.
        '''
        parser = urlparse(url)                                                  # Parse provided URL
        if not parser.netloc:                                                   # Invalid URL
            click.echo('URL is invalid', err=True, color='red')
            url = click.prompt('URL', type=str)                                 # Ask user for base URL
            return RekonoApiCommand._get_url(url)                               # Retry URL validation
        return f'{parser.scheme or "https"}://{parser.netloc}'

    @staticmethod
    def _parse_key_value_params(items: List[str]) -> Dict[str, str]:
        '''Parse key=value options.

        Args:
            items (List[str]): List of key=value values.

        Returns:
            Dict[str, str]: Dictionary with all keys and values.
        '''
        data = {}
        for item in items or []:
            if '=' in item:                                                     # Check separator
                key, value = item.split('=', 1)                                 # Get key and value
                data[key.strip()] = value.strip()
        return data

    @staticmethod
    def _get_body(body: str) -> str:
        '''Validate body value to be sent via HTTP.

        Args:
            body (str): Body value.

        Returns:
            str: Validated body value.
        '''
        if body:
            try:
                json.loads(body)                                                # Try to parse body value
            except json.decoder.JSONDecodeError:                                # Invalid body value
                # TOTEST
                click.echo('Invalid JSON format for body value', err=True, color='red')
                sys.exit(1)
        return body

    @staticmethod
    def _get_endpoint(endpoint: str) -> str:
        '''Get valid endpoint value without parameters or other URL information.

        Args:
            endpoint (str): Endpoint value provided by user.

        Returns:
            str: Valid endpoint value.
        '''
        return urlparse(endpoint).path

    @staticmethod
    def _rekono_factory(url: str, no_verify: bool = False, headers: List[str] = None) -> Rekono:
        '''Create Rekono client entity.

        Args:
            url (str): Base Rekono URL.
            no_verify (bool, optional): Disable TLS validation. Defaults to False.
            headers (List[str], optional): Extra HTTP request headers. Defaults to None.

        Returns:
            Rekono: Rekono API client.
        '''
        api_token = os.getenv(RekonoApiCommand.api_token_env)                   # Get API token from environment
        if api_token:                                                           # API token provided
            return Rekono(                                                      # Create Rekono API client
                RekonoApiCommand._get_url(url),                                 # Get valid Rekono URL
                token=api_token,
                headers=RekonoApiCommand._parse_key_value_params(headers),      # Get HTTP headers
                verify=not no_verify
            )
        username = click.prompt('Username', type=str)                           # Ask for username
        password = click.prompt('Password', type=str, hide_input=True)          # Ask for password
        if not username or not password:                                        # Invalid credentials
            click.echo('Username and password are required', err=True, color='red')
            return RekonoApiCommand._rekono_factory(url, not no_verify, headers)    # Retry Rekono client creation
        try:
            return Rekono(                                                      # Create Rekono API client
                RekonoApiCommand._get_url(url),                                 # Get valid Rekono URL
                username=username,
                password=password,
                headers=RekonoApiCommand._parse_key_value_params(headers),      # Get HTTP headers
                verify=not no_verify
            )
        except AuthenticationError as ex:                                       # Invalid basic credentials
            click.echo(ex.message, err=True, color='red')
            sys.exit(1)

    @staticmethod
    def _get_data_from_responses(responses: List[Response]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        '''Get data from Rekono API responses.

        Args:
            responses (List[Response]): List of Rekono API responses.

        Returns:
            Union[List[Dict[str, Any]], Dict[str, Any]]: Data returned by Rekono.
        '''
        content = []
        for response in responses:                                              # For each response
            try:
                body = response.json()                                          # Parse JSON body from response
            except requests.exceptions.JSONDecodeError:
                continue
            if isinstance(body, dict):                                          # Response body is a dictionary
                body = body.get('results', body)                                # Get results field if it exists
            if isinstance(body, list):                                          # Content is a list
                content.extend(body)                                            # Save content
            elif isinstance(body, dict):                                        # Content is a dictionary
                if len(responses) == 1:                                         # Only one response
                    return body                                                 # Return response content
                content.append(body)                                            # Save content
        return content

    @staticmethod
    def _display_responses(
        responses: List[Response],
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool
    ) -> None:
        '''Display Rekono API responses via standard output.

        Args:
            responses (List[Response]): Rekono API responses.
            show_headers (bool): Display HTTP response headers.
            just_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
        '''
        if quiet:                                                               # No content should be displayed
            return
        if just_show_status_code or show_headers:                               # Headers or status should be displayed
            for response in responses:                                          # For each response
                if just_show_status_code:                                       # Just display status code
                    click.echo(response.status_code, color='red' if response.status_code >= 400 else 'green')
                elif show_headers:                                              # Show response headers
                    click.echo()
                    # Display HTTP request and response summary
                    click.echo(f'{response.request.method} {response.request.path_url} {response.status_code}')
                    for header, value in response.headers.items():
                        click.echo(f'{header}: {value}')                        # Display HTTP response headers
                    click.echo()
                    data = RekonoApiCommand._get_data_from_responses([response])    # Get content from response
                    click.echo(json.dumps(data, ensure_ascii=True, indent=4))   # Display content via standard output
        else:                                                                   # Standard display options
            data = RekonoApiCommand._get_data_from_responses(responses)         # Get content from responses
            click.echo(json.dumps(data, ensure_ascii=True, indent=4))           # Display content via standard output

    @staticmethod
    def _save_output(responses: List[Response], filepath: Optional[str]) -> None:
        '''Save responses content in JSON file.

        Args:
            responses (List[Response]): Rekono API responses.
            filepath (Optional[str]): Filepath to the JSON file where content should be saved.
        '''
        if not filepath:                                                        # JSON filepath is provided
            return
        data = RekonoApiCommand._get_data_from_responses(responses)             # Get data from responses
        with open(filepath, 'w', encoding='utf-8') as file:                     # Open JSON file
            json.dump(data, file, ensure_ascii=True, indent=4)                  # Write content in JSON file

    @click.command(help='GET request to Rekono API')
    @endpoint_argument
    @url_option
    @headers_option
    @parameters_option
    @no_verify_option
    @all_pages_option
    @show_headers_option
    @status_code_option
    @quiet_option
    @json_option
    def get(
        endpoint: str,
        url: str,
        headers: List[str],
        parameters: List[str],
        no_verify: bool,
        all_pages: bool,
        show_headers: bool,
        just_show_status_code: bool,
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
            all_pages (bool): Enable iteration over all API pages.
            show_headers (bool): Display HTTP response headers.
            just_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response_or_responses = client.get(
            RekonoApiCommand._get_endpoint(endpoint),
            parameters=RekonoApiCommand._parse_key_value_params(parameters),
            all_pages=all_pages
        )
        responses = response_or_responses if isinstance(response_or_responses, list) else [response_or_responses]
        RekonoApiCommand._display_responses(responses, show_headers, just_show_status_code, quiet)
        RekonoApiCommand._save_output(responses, json_output)

    @click.command(help='POST request to Rekono API')
    @endpoint_argument
    @url_option
    @headers_option
    @body_option
    @no_verify_option
    @show_headers_option
    @status_code_option
    @quiet_option
    @json_option
    def post(
        endpoint: str,
        url: str,
        headers: List[str],
        body: str,
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool,
        json_output: str
    ):
        '''POST request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            body (str): HTTP body to send in JSON format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            just_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response = client.post(RekonoApiCommand._get_endpoint(endpoint), RekonoApiCommand._get_body(body))
        RekonoApiCommand._display_responses([response], show_headers, just_show_status_code, quiet)
        RekonoApiCommand._save_output([response], json_output)

    @click.command(help='PUT request to Rekono API')
    @endpoint_argument
    @url_option
    @headers_option
    @body_option
    @no_verify_option
    @show_headers_option
    @status_code_option
    @quiet_option
    @json_option
    def put(
        endpoint: str,
        url: str,
        headers: List[str],
        body: str,
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool,
        json_output: str
    ):
        '''PUT request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            body (str): HTTP body to send in JSON format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            just_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
            json_output (str): Filepath to the JSON file where content should be saved.
        '''
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response = client.put(RekonoApiCommand._get_endpoint(endpoint), RekonoApiCommand._get_body(body))
        RekonoApiCommand._display_responses([response], show_headers, just_show_status_code, quiet)
        RekonoApiCommand._save_output([response], json_output)

    @click.command(help='DELETE request to Rekono API')
    @endpoint_argument
    @url_option
    @headers_option
    @no_verify_option
    @show_headers_option
    @status_code_option
    @quiet_option
    def delete(
        endpoint: str,
        url: str,
        headers: List[str],
        no_verify: bool,
        show_headers: bool,
        just_show_status_code: bool,
        quiet: bool
    ):
        '''DELETE request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            url (str): Rekono base URL.
            headers (List[str]): HTTP headers to send in key=value format.
            no_verify (bool): Disable TLS validation.
            show_headers (bool): Display HTTP response headers.
            just_show_status_code (bool): Just display HTTP response status code.
            quiet (bool): Don't display anything from response.
        '''
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response = client.delete(RekonoApiCommand._get_endpoint(endpoint))
        RekonoApiCommand._display_responses([response], show_headers, just_show_status_code, quiet)
