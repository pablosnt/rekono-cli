import click
from install.command import install


@click.group()
def rekono():
    '''Rekono CLI.'''
    pass


# Add Rekono commands
rekono.add_command(install)


if __name__ == '__main__':
    rekono()
