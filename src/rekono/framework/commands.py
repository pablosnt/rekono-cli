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

    api_token_env = 'REKONO_TOKEN'
    commands = ['get', 'post', 'put', 'delete']

    def list_commands(self, ctx: click.Context) -> List[str]:
        return self.commands

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        return getattr(self, cmd_name) if hasattr(self, cmd_name) else None

    @staticmethod
    def _get_url(url: str) -> str:
        parser = urlparse(url)
        if not parser.netloc:
            click.echo('URL is invalid', err=True, color='red')
            url = click.prompt('URL', type=str)
            return RekonoApiCommand._get_url(url)
        return f'{parser.scheme or "https"}://{parser.netloc}'

    @staticmethod
    def _parse_key_value_params(items: List[str]) -> Dict[str, str]:
        data = {}
        for item in items or []:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()
        return data

    @staticmethod
    def _get_body(body: str) -> Dict[str, Any]:
        if body:
            try:
                json.loads(body)
            except json.decoder.JSONDecodeError:
                click.echo('Invalid JSON format for body value', err=True, color='red')
                sys.exit(1)
        return body

    @staticmethod
    def _get_endpoint(endpoint: str) -> str:
        return urlparse(endpoint).path

    @staticmethod
    def _rekono_factory(url:  str, no_verify: bool = False, headers: List[str] = None) -> Rekono:
        api_token = os.getenv(RekonoApiCommand.api_token_env)
        if api_token:
            return Rekono(
                RekonoApiCommand._get_url(url),
                token=api_token,
                headers=RekonoApiCommand._parse_key_value_params(headers),
                verify=not no_verify
            )
        username = click.prompt('Username', type=str)
        password = click.prompt('Password', type=str, hide_input=True)
        if not username or not password:
            click.echo('Username and password are required', err=True, color='red')
            return RekonoApiCommand._rekono_factory(url, not no_verify, headers)
        try:
            return Rekono(
                RekonoApiCommand._get_url(url),
                username=username,
                password=password,
                headers=RekonoApiCommand._parse_key_value_params(headers),
                verify=not no_verify
            )
        except AuthenticationError as ex:
            click.echo(ex.message, err=True, color='red')
            sys.exit(1)

    @staticmethod
    def _get_data_from_responses(responses: List[Response]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        all_data = []
        for response in responses:
            try:
                body = response.json()
            except requests.exceptions.JSONDecodeError:
                continue
            if isinstance(body, dict):
                body = body.get('results', body)
            if isinstance(body, list):
                all_data.extend(body)
            elif isinstance(body, dict):
                if len(responses) == 1:
                    return body
                all_data.append(body)
        return all_data

    @staticmethod
    def _display_responses(responses: List[Response], show_headers: bool, just_show_status_code: bool, quiet: bool) -> None:
        if quiet:
            return
        if just_show_status_code or show_headers:
            for response in responses:
                if just_show_status_code:
                    click.echo(response.status_code, color='red' if response.status_code >= 400 else 'green')
                elif show_headers:
                    click.echo()
                    click.echo(f'{response.request.method} {response.request.path_url} {response.status_code}')
                    for header, value in response.headers.items():
                        click.echo(f'{header}: {value}')
                    click.echo()
                    data = RekonoApiCommand._get_data_from_responses([response])
                    if isinstance(data, dict) or isinstance(data, list):
                        click.echo(json.dumps(data, ensure_ascii=True, indent=4))
        else:
            data = RekonoApiCommand._get_data_from_responses(responses)
            click.echo(json.dumps(data, ensure_ascii=True, indent=4))

    @staticmethod
    def _save_output(responses: List[Response], filepath: Optional[str]) -> None:
        if not filepath:
            return
        data = RekonoApiCommand._get_data_from_responses(responses)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=True, indent=4)

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
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        responses = client.get(
            RekonoApiCommand._get_endpoint(endpoint),
            parameters=RekonoApiCommand._parse_key_value_params(parameters),
            all_pages=all_pages
        )
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
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response = client.post(
            RekonoApiCommand._get_endpoint(endpoint),
            RekonoApiCommand._get_body(body)
        )
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
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response = client.put(
            RekonoApiCommand._get_endpoint(endpoint),
            RekonoApiCommand._get_body(body)
        )
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
        client = RekonoApiCommand._rekono_factory(url, no_verify, headers)
        response = client.delete(RekonoApiCommand._get_endpoint(endpoint))
        RekonoApiCommand._display_responses([response], show_headers, just_show_status_code, quiet)
