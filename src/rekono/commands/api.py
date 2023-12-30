"""Command to make custom Rekono API requests."""

import click

from rekono.framework.commands.api import ApiCommand


@click.group("api", cls=ApiCommand)
def api():
    """Make custom Rekono API requests."""
