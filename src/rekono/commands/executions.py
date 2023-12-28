"""CLI command to manage Execution entities."""

import click

from rekono.framework.commands.entity import EntityCommand


class ExecutionsCommand(EntityCommand):
    """CLI command to manage Execution entities."""

    commands = ["get"]  # CLI commands
    # Help messages for each command
    help_messages = {
        "get": "Get all executions or one if ID is provided",
    }


@click.group("executions", cls=ExecutionsCommand)
def executions():
    """Get executions"""
