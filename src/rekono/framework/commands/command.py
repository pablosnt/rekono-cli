'''Base features for Rekono CLI command.'''

import json
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Union, cast
from urllib.parse import urlparse

import click
import requests
from requests.models import Response

from rekono.client.api import Rekono


class RekonoCliCommand(click.MultiCommand):
    '''Base features for Rekono CLI command.'''

    # Environment variables
    api_token_env = 'REKONO_TOKEN'                                              # Environment variable to set API token
    backend_url_env = 'REKONO_URL'                                              # Environment variable to set backend
    # Initialization of variables
    commands: List[str] = []                                                    # List of supported commands
    commands_mapping: Dict[str, str] = {}                                       # Mapping between commands and methods
    default_mapping: Optional[str] = None                                       # Default method if mapping not found
    help_messages: Dict[str, str] = {}                                          # Help messages for each command
    api_options: List[Callable] = []                                            # API options for all commands
    display_options: List[Callable] = []                                        # Display options for all commands
    entity_options: List[Callable] = []                                         # Specific options for post and put

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
        related_command_method = self.commands_mapping.get(cmd_name, self.default_mapping)      # Get mapped method
        if cmd_name in self.commands and related_command_method and hasattr(self, related_command_method):
            command: click.Command = getattr(self, related_command_method)      # Get command method
            command.help = self.help_messages.get(cmd_name)                     # Set help message
            if related_command_method in ['post_entity', 'put_entity']:         # POST or PUT entity request
                self._apply_command_options(command, self.entity_options)       # Set entity options
            self._apply_command_options(command, self.api_options)              # Set base API options
            self._apply_command_options(command, self.display_options)          # Set base display options
            return command
        return None

    def _apply_command_options(self, command: Callable, options: List[Callable]) -> Callable:
        '''Apply multiple options to specific command.

        Args:
            command (Callable): Command to configure
            options (List[Callable]): List of options to apply

        Returns:
            Callable: Configured command
        '''
        for option in options:
            command = option(command)
        return command

    @classmethod
    def _get_url(cls, url: str) -> str:
        '''Get valid Rekono base URL from the user provided value.

        Args:
            url (str): User provided URL.

        Returns:
            str: Valid Rekono URL.
        '''
        parser = urlparse(url)                                                  # Parse provided URL
        if not parser.netloc:                                                   # Invalid URL
            click.echo(click.style('URL is invalid', fg='red'), err=True, color=True)
            url = click.prompt('URL', type=str)                                 # Ask user for base URL
            return cls._get_url(url)                                            # Retry URL validation
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
    def _get_body(body: Optional[str]) -> Optional[str]:
        '''Validate body value to be sent via HTTP.

        Args:
            body (Optional[str]): Body value.

        Returns:
            Optional[str]: Validated body value.
        '''
        if body:
            try:
                json.loads(body)                                                # Try to parse body value
            except json.decoder.JSONDecodeError:                                # Invalid body value
                click.echo(click.style('Invalid JSON format for body value', fg='red'), err=True, color=True)
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

    @classmethod
    def _rekono_factory(cls, url: str, no_verify: bool = False, headers: List[str] = []) -> Rekono:
        '''Create Rekono client entity.

        Args:
            url (str): Base Rekono URL.
            no_verify (bool, optional): Disable TLS validation. Defaults to False.
            headers (List[str], optional): Extra HTTP request headers. Defaults to [].

        Returns:
            Rekono: Rekono API client.
        '''
        token = os.getenv(cls.api_token_env)                                    # Get API token from environment
        if not token:                                                           # API token is not provided
            token = click.prompt('API token', type=str, hide_input=True)        # Ask for API token
        return Rekono(                                                          # Create Rekono API client
            cls._get_url(url),                                                  # Get valid Rekono URL
            token=cast(str, token),
            headers=cls._parse_key_value_params(headers),                       # Get HTTP headers
            verify=not no_verify
        )

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

    @classmethod
    def _display_responses(
        cls,
        responses: List[Response],
        show_headers: bool,
        only_show_status_code: bool,
        quiet: bool
    ) -> None:
        '''Display Rekono API responses via standard output.

        Args:
            responses (List[Response]): Rekono API responses.
            show_headers (bool): Display HTTP response headers.
            only_show_status_code (bool): Only display status code from HTTP response.
            quiet (bool): Don't display anything from response.
        '''
        if quiet:                                                               # No content should be displayed
            return
        if only_show_status_code or show_headers:                               # Headers or status should be displayed
            for response in responses:                                          # For each response
                if only_show_status_code:                                       # Just display status code
                    click.echo(response.status_code)
                elif show_headers:                                              # Show response headers
                    click.echo()
                    # Display HTTP request and response summary
                    click.echo(f'{response.request.method} {response.request.path_url} {response.status_code}')
                    for header, value in response.headers.items():
                        click.echo(f'{header}: {value}')                        # Display HTTP response headers
                    click.echo()
                    data = cls._get_data_from_responses([response])             # Get content from response
                    click.echo(json.dumps(data, ensure_ascii=True, indent=4))   # Display content via standard output
        else:                                                                   # Standard display options
            data = cls._get_data_from_responses(responses)                      # Get content from responses
            click.echo(json.dumps(data, ensure_ascii=True, indent=4))           # Display content via standard output

    @classmethod
    def _save_output(cls, responses: List[Response], filepath: Optional[str]) -> None:
        '''Save responses content in JSON file.

        Args:
            responses (List[Response]): Rekono API responses.
            filepath (Optional[str]): Filepath to the JSON file where content should be saved.
        '''
        if not filepath:                                                        # JSON filepath isn't provided
            return
        data = cls._get_data_from_responses(responses)                          # Get data from responses
        with open(filepath, 'w', encoding='utf-8') as file:                     # Open JSON file
            json.dump(data, file, ensure_ascii=True, indent=4)                  # Write content in JSON file
