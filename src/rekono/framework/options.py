'''Definition of CLI options.'''

from typing import Callable, List

import click

url_option = click.option(                                                      # URL option
    '-u', '--url', 'url',
    type=str, required=False,
    default='http://127.0.0.1:8000',
    help='Base URL to the Rekono backend'
)

headers_option = click.option(                                                  # Extra request header option
    '-h', '--header', 'headers',
    multiple=True, type=str,
    required=False, default=[],
    help='HTTP header to send in format "<key>=value"'
)

no_verify_option = click.option(                                                # Option to disable TLS verification
    '--no-verify', 'no_verify',
    is_flag=True, default=False,
    help='Disable TLS verification'
)

parameters_option = click.option(                                               # Request parameter option
    '-p', '--parameter', 'parameters',
    multiple=True, type=str,
    required=False, default=[],
    help='HTTP parameter to send in format "<key>=value"'
)

body_option = click.option(                                                     # Request body option
    '-b', '--body', 'body',
    type=str, required=False,
    help='HTTP body to send in JSON'
)

file_option = click.option(
    '-f', '--file', 'filepath',
    type=click.Path(exists=True),
    required=False, default=None,
    help='File to upload'
)

all_pages_option = click.option(                                                # Option to iterate over all API pages
    '-a', '--all-pages', 'all_pages',
    is_flag=True, default=False,
    help='Perform pagination over all pages'
)

show_headers_option = click.option(                                             # Option to show response headers
    '-s', '--show-headers', 'show_headers',
    is_flag=True, default=False,
    help='Show response headers'
)

show_status_code_option = click.option(                                         # Option to only show response status
    '--status-code', 'just_show_status_code',
    is_flag=True, default=False,
    help='Just show response status code'
)

quiet_option = click.option(                                                    # Option to don't show anything
    '--quiet', 'quiet',
    is_flag=True, default=False,
    help='Don\'t show anything from response'
)

json_option = click.option(                                                     # JSON output option
    '-j', '--json', 'json_output',
    type=str, required=False,
    help='Save response data in JSON file'
)

tags_option = click.option(
    '-t', '--tag', 'tags',
    multiple=True, type=str,
    required=False, default=[],
    help='Related tags'
)
