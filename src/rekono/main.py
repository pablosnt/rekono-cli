'''Main Rekono CLI exectuable.'''

import click

from rekono import VERSION
from rekono.commands.api import api


@click.group()
@click.version_option(version=VERSION, message='%(version)s')
def rekono():
    '''Rekono CLI.'''


# Add CLI commands
rekono.add_command(api)


if __name__ == '__main__':
    rekono()
