import click

from rekono import VERSION
from rekono.api.commands import api


@click.group()
@click.version_option(version=VERSION, message='%(version)s')
def rekono():
    '''Rekono CLI.'''
    pass


# Add Rekono commands
rekono.add_command(api)


if __name__ == '__main__':
    rekono()
