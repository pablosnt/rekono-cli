"""CLI command to manage Configuration entities."""

import click

from rekono.framework.commands.entity import EntityCommand


class ConfigurationsCommand(EntityCommand):
    """CLI command to manage Configuration entities."""

    commands = ["get"]  # CLI commands
    # Help messages for each command
    help_messages = {
        "get": "Get all configurations or one if ID is provided",
    }


@click.group("configurations", cls=ConfigurationsCommand)
def configurations():
    """Get configurations."""
