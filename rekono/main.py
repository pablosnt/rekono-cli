import click
from install.commands import install
from services.commands import services


@click.group()
def rekono():
    '''Rekono CLI.'''
    pass


# Add Rekono commands
rekono.add_command(install)
rekono.add_command(services)


if __name__ == '__main__':
    rekono()
