'''Definition of base CLI arguments used by multiple commands.'''

import click

endpoint_argument = click.argument('endpoint', type=str, nargs=1)               # Endpoint argument

id_optional_argument = click.argument('id', type=int, nargs=1, required=False)  # Id optional argument

id_mandatory_argument = click.argument('id', type=int, nargs=1)                 # Id mandatory argument
