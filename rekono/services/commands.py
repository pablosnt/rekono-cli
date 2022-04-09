import sys

import click

from rekono.installation.check import check_rekono_installation
from rekono.services.manager import rekono_services_command
from rekono.services.services import EXECUTIONS
from rekono.utils.linux.check import check_system
from rekono.utils.linux.systemctl import (count_running_services,
                                          systemctl_command)


@click.group('services', help='Manage Rekono systemctl services')
def services():
    '''Manage Rekono systemctl services.'''
    check_system()                                                              # Check if it is a Linux system
    if not check_rekono_installation():                                         # Check if Rekono is installed
        click.echo(
            click.style('Rekono is not installed on the system. Please, run the command install', fg='red'), err=True
        )
        sys.exit(1)


@services.command('start', help='Start Rekono services')
@click.option(
    '-e', '--execution-workers', 'executors',
    type=int, required=False, default=3,
    help='Number of workers for executions queue'
)
def start(executors: int):
    '''Start all Rekono services.

    Args:
        executors (int): Number of workers for executions queue.
    '''
    if executors < 0:
        click.echo(click.style('Number of workers should be greater than zero', fg='red'), err=True)
        sys.exit(100)
    elif executors == 0:
        click.echo(
            click.style('Number of workers is zero so executions are disabled', fg='orange')
        )
    systemctl_command('start', 'postgresql')                                    # Start PostgreSQL
    systemctl_command('start', 'redis-server')                                  # Start Redis
    rekono_services_command('start', executors)


@services.command('stop', help='Stop Rekono services')
def stop():
    '''Stop all Rekono services.'''
    executors = count_running_services(f'rekono-{EXECUTIONS}')
    rekono_services_command('stop', executors)


@services.command('restart', help='Restart Rekono services')
def restart():
    '''Restart all Rekono services.'''
    executors = count_running_services(f'rekono-{EXECUTIONS}')
    rekono_services_command('restart', executors)
