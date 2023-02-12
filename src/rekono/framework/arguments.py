'''Definition of CLI arguments.'''

import click

endpoint_argument = click.argument('endpoint', type=str, nargs=1)               # Endpoint argument
