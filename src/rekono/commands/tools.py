"""CLI command to manage Tool entities."""

import click

from rekono.framework.commands.entity import EntityCommand


class ToolsCommand(EntityCommand):
    """CLI command to manage Tool entities."""

    commands = ["get"]  # CLI commands
    # Help messages for each command
    help_messages = {
        "get": "Get all tools or one if ID is provided",
    }


@click.group("tools", cls=ToolsCommand)
def tools():
    """Get tools."""
