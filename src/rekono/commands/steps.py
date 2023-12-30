"""CLI command to manage Step entities."""

import click

from rekono.framework.commands.entity import EntityCommand


class StepsCommand(EntityCommand):
    """CLI command to manage Step entities."""

    # Help messages for each command
    help_messages = {
        "get": "Get all steps or one if ID is provided",
        "create": "Create step",
        "update": "Update step",
        "delete": "Delete step",
    }
    # Specific options for post and put
    entity_options = [
        click.option(
            "-p", "--process", "process", required=True, type=int, help="Process ID"
        ),
        click.option(
            "-t", "--tool", "tool_id", required=True, type=int, help="Tool ID"
        ),
        click.option(
            "-c",
            "--configuration",
            "configuration_id",
            required=True,
            type=int,
            help="Configuration ID",
        ),
        click.option(
            "--priority",
            "priority",
            required=False,
            default=1,
            type=int,
            help="Step priority within process",
        ),
    ]


@click.group("steps", cls=StepsCommand)
def steps():
    """Manage steps."""
