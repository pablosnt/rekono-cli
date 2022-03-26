import platform
import sys

import click


@click.command('install', help='Install Rekono in the system')
def install():
    '''Install Rekono in the system.'''
    if platform.system().lower() == 'linux':
        # Local installation is only available for Linux
        pass
        # Clone source code in directory (/opt/rekono)
        # Install packages and technologies required: RQ, Node, NPM, Postgresql
        #   -> (if RQ or Postgresal exists, ask for credentials)
        # Install Django dependencies
        # Install Vue dependencies
        # Initialize database
        # Create configuration
        # Initialize REKONO_HOME (/usr/share/rekono)
        # Create Linux services (ask for start them)
    else:
        click.echo(click.style('Installation only works in Linux systems', fg='red'))
        click.echo('For this system, you can follow this steps to deploy Rekono in Docker: ')
        sys.exit(1)
