"""Main Rekono CLI exectuable."""

from typing import Type

import click

from rekono import VERSION
from rekono.commands.api import api
from rekono.commands.authentications import authentications
from rekono.commands.configurations import configurations
from rekono.commands.executions import executions
from rekono.commands.findings import (
    credentials,
    exploits,
    hosts,
    osint,
    paths,
    ports,
    technologies,
    vulnerabilities,
)
from rekono.commands.processes import processes
from rekono.commands.profile import profile
from rekono.commands.projects import projects
from rekono.commands.settings import settings
from rekono.commands.steps import steps
from rekono.commands.target_ports import target_ports
from rekono.commands.targets import targets
from rekono.commands.tasks import tasks
from rekono.commands.tools import tools
from rekono.commands.users import users
from rekono.commands.wordlists import wordlists


@click.group()
@click.version_option(version=VERSION, message="%(version)s")
def rekono():
    """Rekono CLI."""


typed_rekono: Type[click.Group] = rekono

# Add CLI commands
typed_rekono.add_command(api)
typed_rekono.add_command(authentications)
typed_rekono.add_command(configurations)
typed_rekono.add_command(credentials)
typed_rekono.add_command(executions)
typed_rekono.add_command(exploits)
typed_rekono.add_command(hosts)
typed_rekono.add_command(osint)
typed_rekono.add_command(paths)
typed_rekono.add_command(ports)
typed_rekono.add_command(processes)
typed_rekono.add_command(profile)
typed_rekono.add_command(projects)
typed_rekono.add_command(settings)
typed_rekono.add_command(steps)
typed_rekono.add_command(target_ports)
typed_rekono.add_command(targets)
typed_rekono.add_command(tasks)
typed_rekono.add_command(technologies)
typed_rekono.add_command(tools)
typed_rekono.add_command(users)
typed_rekono.add_command(vulnerabilities)
typed_rekono.add_command(wordlists)


if __name__ == "__main__":
    rekono()
