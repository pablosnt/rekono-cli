"""CLI command to manage TargetPort entities."""

import click

from rekono.framework.commands.entity import EntityCommand


class TargetPortsCommand(EntityCommand):
    """CLI command to manage TargetPort entities."""

    commands = ["get", "create", "delete"]  # CLI commands
    # Help messages for each command
    help_messages = {
        "get": "Get all target ports or one if ID is provided",
        "create": "Create target port",
        "delete": "Delete target port",
    }
    # Specific options for post and put
    entity_options = [
        click.option(
            "-t", "--target", "target", required=True, type=int, help="Target ID"
        ),
        click.option(
            "-p", "--port", "port", required=True, type=int, help="Port number"
        ),
    ]


@click.group("target-ports", cls=TargetPortsCommand)
def target_ports():
    """Manage target ports."""
