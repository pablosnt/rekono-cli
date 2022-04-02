import platform
import sys

import click


def check_system() -> None:
    '''Check if the system is Linux.'''
    if platform.system().lower() != 'linux':
        click.echo(
            click.style('Rekono installation and services management only work in Linux systems', fg='red'), err=True
        )
        click.echo(
            'For this system, you can follow this steps to deploy '
            'Rekono in Docker: https://github.com/pablosnt/rekono#docker'
        )
        sys.exit(1)
