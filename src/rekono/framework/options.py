"""Definition of base CLI options used by multiple commands."""

from pathlib import Path
from typing import Callable

import click

from rekono.framework.commands.command import RekonoCliCommand

# URL option
url_option: Callable = click.option(
    "-u",
    "--url",
    "url",
    type=str,
    required=False,
    envvar=RekonoCliCommand.backend_url_env,
    default="http://127.0.0.1:8000",
    help="Base URL to the Rekono backend",
)

# Extra request headers option
headers_option: Callable = click.option(
    "-h",
    "--header",
    "headers",
    multiple=True,
    type=str,
    required=False,
    default=[],
    help='HTTP header to send in format "<key>=value"',
)

# Option to disable TLS verification
no_verify_option: Callable = click.option(
    "--no-verify",
    "no_verify",
    is_flag=True,
    default=False,
    help="Disable TLS verification",
)

# Request parameters option
parameters_option: Callable = click.option(
    "-p",
    "--parameter",
    "parameters",
    multiple=True,
    type=str,
    required=False,
    default=[],
    help='HTTP parameter to send in format "<key>=value"',
)

# Request body option
body_option: Callable = click.option(
    "-b", "--body", "body", type=str, required=False, help="HTTP body to send in JSON"
)

# Filepath to upload option
file_option: Callable = click.option(
    "-f",
    "--file",
    "filepath",
    type=click.Path(exists=True, path_type=Path),
    required=False,
    default=None,
    help="File to upload",
)

# Option to iterate over all API pages
all_pages_option: Callable = click.option(
    "-a",
    "--all-pages",
    "pagination",
    is_flag=True,
    default=False,
    help="Perform pagination over all pages",
)

# Option to show response headers
show_headers_option: Callable = click.option(
    "-s",
    "--show-headers",
    "show_headers",
    is_flag=True,
    default=False,
    help="Show response headers",
)

# Option to only show response status
show_status_code_option: Callable = click.option(
    "--status-code",
    "only_show_status_code",
    is_flag=True,
    default=False,
    help="Only show response status code",
)

# Option to don't show anything
quiet_option: Callable = click.option(
    "--quiet",
    "quiet",
    is_flag=True,
    default=False,
    help="Don't show anything from response",
)

# JSON output option
json_option: Callable = click.option(
    "-j",
    "--json",
    "json_output",
    type=str,
    required=False,
    help="Save response data in JSON file",
)

# Tags option used by multiple commands
tags_option: Callable = click.option(
    "-t",
    "--tag",
    "tags",
    multiple=True,
    type=str,
    required=False,
    default=[],
    help="Related tags",
)
