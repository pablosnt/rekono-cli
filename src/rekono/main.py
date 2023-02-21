'''Main Rekono CLI exectuable.'''

import click

from rekono import VERSION
from rekono.commands.api import api
from rekono.commands.authentications import authentications
from rekono.commands.executions import executions
from rekono.commands.findings import (credentials, exploits, hosts, osint,
                                      paths, ports, technologies,
                                      vulnerabilities)
from rekono.commands.projects import projects
from rekono.commands.tools import configurations, tools


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
rekono.add_command(projects)
rekono.add_command(technologies)
rekono.add_command(tools)
rekono.add_command(vulnerabilities)


if __name__ == '__main__':
    rekono()
