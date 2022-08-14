import click

from rekono.api.commands import api
from rekono.installation.commands import install, uninstall, update
from rekono.services.commands import services


@click.group()
def rekono():
    '''Rekono CLI.'''
    pass


# Add Rekono commands
rekono.add_command(install)
rekono.add_command(update)
rekono.add_command(uninstall)
rekono.add_command(services)
rekono.add_command(api)


if __name__ == '__main__':
    rekono()
