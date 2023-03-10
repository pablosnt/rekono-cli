'''Main Rekono CLI exectuable.'''

import click

from rekono import VERSION
from rekono.commands.api import api
from rekono.commands.authentications import authentications
from rekono.commands.configurations import configurations
from rekono.commands.executions import executions
from rekono.commands.findings import (credentials, exploits, hosts, osint,
                                      paths, ports, technologies,
                                      vulnerabilities)
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
@click.version_option(version=VERSION, message='%(version)s')
def rekono():
    '''Rekono CLI.'''


# Add CLI commands
rekono.add_command(api)
rekono.add_command(authentications)
rekono.add_command(configurations)
rekono.add_command(credentials)
rekono.add_command(executions)
rekono.add_command(exploits)
rekono.add_command(hosts)
rekono.add_command(osint)
rekono.add_command(paths)
rekono.add_command(ports)
rekono.add_command(processes)
rekono.add_command(profile)
rekono.add_command(projects)
rekono.add_command(settings)
rekono.add_command(steps)
rekono.add_command(target_ports)
rekono.add_command(targets)
rekono.add_command(tasks)
rekono.add_command(technologies)
rekono.add_command(tools)
rekono.add_command(users)
rekono.add_command(vulnerabilities)
rekono.add_command(wordlists)


if __name__ == '__main__':
    rekono()
