"""CLI command to manage findings entities."""

import click

from rekono.framework.commands.entity import EntityCommand


class FindingsCommand(EntityCommand):
    """CLI command to manage findings entities."""

    commands = ["get", "enable", "disable"]  # CLI commands
    # Mapping between commands and methods
    commands_mapping = {
        "get": "get_entity",
        "disable": "delete_entity",
    }
    # Help messages for each command
    help_messages = {
        "get": "Get all findings or one if ID is provided",
        "enable": "Enable finding",
        "disable": "Disable finding",
    }


@click.group("credentials", cls=FindingsCommand)
def credentials():
    """Manage credentials."""


@click.group("exploits", cls=FindingsCommand)
def exploits():
    """Manage exploits."""


@click.group("hosts", cls=FindingsCommand)
def hosts():
    """Manage hosts."""


@click.group("paths", cls=FindingsCommand)
def paths():
    """Manage paths."""


@click.group("ports", cls=FindingsCommand)
def ports():
    """Manage ports."""


@click.group("technologies", cls=FindingsCommand)
def technologies():
    """Manage technologies."""


@click.group("vulnerabilities", cls=FindingsCommand)
def vulnerabilities():
    """Manage vulnerabilities."""


class OSINTCommand(FindingsCommand):
    """CLI command to manage OSINT entities."""

    commands = ["get", "enable", "disable", "target"]  # Supported CLI commands
    # Help messages for each command
    help_messages = {
        "get": "Get all findings or one if ID is provided",
        "enable": "Enable finding",
        "disable": "Disable finding",
        "target": "Create target from OSINT data",
    }


@click.group("osint", cls=OSINTCommand)
def osint():
    """Manage OSINT findings."""
