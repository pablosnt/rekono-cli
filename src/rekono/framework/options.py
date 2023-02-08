import click

url_option = click.option(
    '-u', '--url', 'url',
    type=str, required=False,
    default='http://127.0.0.1:8000',
    help='Base URL to the Rekono backend'
)

headers_option = click.option(
    '-h', '--header', 'headers',
    multiple=True, type=str,
    required=False, default=[],
    help='HTTP header to send in format "<key>=value"'
)

parameters_option = click.option(
    '-p', '--parameter', 'parameters',
    multiple=True, type=str,
    required=False, default=[],
    help='HTTP parameter to send in format "<key>=value"'
)

body_option = click.option(
    '-b', '--body', 'body',
    multiple=False, type=str, required=False,
    help='HTTP body to send in JSON format'
)

no_verify_option = click.option(
    '-n', '--no-verify', 'no_verify',
    is_flag=True, default=False,
    help='Disable TLS verification'
)

all_pages_option = click.option(
    '-a', '--all-pages', 'all_pages',
    is_flag=True, default=False,
    help='Perform pagination over all pages'
)

show_headers_option = click.option(
    '-S', '--show-headers', 'show_headers',
    is_flag=True, default=False,
    help='Show response headers'
)

status_code_option = click.option(
    '-s', '--status-code', 'just_show_status_code',
    is_flag=True, default=False,
    help='Just show response status code'
)

quiet_option = click.option(
    '-q', '--quiet', 'quiet',
    is_flag=True, default=False,
    help='Don\'t show anything from response'
)

json_option = click.option(
    '-j', '--json', 'json_output',
    type=str, required=False,
    help='Save response data in JSON file'
)
