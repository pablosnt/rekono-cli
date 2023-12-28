"""Definition of base CLI arguments used by multiple commands."""

from typing import Callable

import click

# Endpoint argument
endpoint_argument: Callable = click.argument("endpoint", type=str, nargs=1)

# Id optional argument
id_optional_argument: Callable = click.argument("id", type=int, nargs=1, required=False)

# Id mandatory argument
id_mandatory_argument: Callable = click.argument("id", type=int, nargs=1)
