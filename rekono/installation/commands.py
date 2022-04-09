import os
import subprocess
import sys

import click

from rekono.config import REKONO_HOME_DIRECTORY
from rekono.installation.check import check_rekono_installation
from rekono.installation.configuration import create_config_file
from rekono.installation.dependencies import (drop_rekono_database,
                                              install_backend,
                                              install_frontend,
                                              install_postgresql, install_rq,
                                              install_vue)
from rekono.installation.management import manage_command
from rekono.installation.tools import (configure_tools, install_resources,
                                       install_tools)
from rekono.services.commands import start
from rekono.services.manager import (create_rekono_services,
                                     rekono_services_command,
                                     remove_rekono_services)
from rekono.services.services import EXECUTIONS
from rekono.utils.linux.apt import apt_install, apt_update
from rekono.utils.linux.check import check_system
from rekono.utils.linux.systemctl import (count_running_services,
                                          reload_systemctl)
from rekono.utils.linux.users import create_rekono_user, remove_rekono_user
from rekono.utils.source_code.rekono import download_source_code


@click.command('install', help='Install Rekono on the system')
@click.option(
    '-a', '--all-tools', 'all_tools', is_flag=True,
    help='Install all tools and resources supported by Rekono'
)
def install(all_tools: bool):
    '''Install Rekono on the system.

    Args:
        all_tools (bool): Indicate if all tools supported by Rekono should be installed or not
    '''
    check_system()                                                              # Check if it is a Linux system
    if check_rekono_installation():                                             # Check if Rekono is already installed
        click.echo(click.style('Rekono is already installed on the system', fg='green'))
        sys.exit(0)
    if os.path.isdir(REKONO_HOME_DIRECTORY):                                    # Rekono directory already exists
        click.echo(click.style(
            f'{REKONO_HOME_DIRECTORY} already exists. Please, set the directory where Rekono '
            'should be downloaded, using the environment variable "REKONO_HOME"', fg='red'
        ), err=True)
        sys.exit(1)
    click.echo('Downloading Rekono source code')
    download_source_code()                                                      # Download Rekono source code
    click.echo()
    click.echo('Installing Rekono dependencies')
    apt_update()                                                                # Update APT sources
    click.echo('[+] PostgreSQL')
    db_password = install_postgresql()                                          # Install PostgreSQL
    click.echo('[+] Redis')
    install_rq()                                                                # Install Redis Queue
    click.echo('[+] Vue')
    install_vue()                                                               # Install Vue
    click.echo('[+] Other packages')
    apt_install(['libpq-dev', 'python3-dev'])                                   # Install other dependencies
    click.echo('[+] Rekono backend dependencies')
    install_backend()                                                           # Install backend dependencies
    click.echo('[+] Rekono frontend dependencies')
    install_frontend()                                                          # Install frontend dependencies
    click.echo()
    click.echo('Configuring Rekono')
    click.echo("Don't worry if you can't configure some items, press ENTER")
    create_config_file(db_password)                                             # Create Rekono configuration
    click.echo()
    manage_command('migrate')                                                   # Migrate Rekono database
    click.echo()
    click.echo('Creation first Rekono user')
    manage_command('createsuperuser')                                           # Create Rekono superuser
    manage_command('frontend')                                                  # Configure Rekono frontend
    if all_tools:
        click.echo()
        click.echo('Installing all supported tools')
        install_tools()
        configure_tools()
        click.echo('Installing all supported resources')
        install_resources()
    click.echo()
    click.echo('Creating systemd services for Rekono')
    create_rekono_user()
    create_rekono_services()                                                    # Create Rekono services
    reload_systemctl()                                                          # Reload Systemctl daemon
    click.echo()
    click.echo(click.style('Installation completed!', fg='green'))
    answer = input('Do you want to start Rekono services? [Y/N]: ')
    if answer.lower() in ['y', 'yes']:
        answer = input('How many execution workers do you need? [3]: ')
        try:
            execution_workers = int(answer)
        except ValueError:
            execution_workers = 3
        start(executors=execution_workers)                                      # Start Rekono services


@click.command('update', help='Update Rekono installation with the latest version')
def update():
    '''Update Rekono installation with the latest version.'''
    check_system()                                                              # Check if it is a Linux system
    if not check_rekono_installation():                                         # Check if Rekono is installed
        click.echo(
            click.style('Rekono is not installed on the system. Please, run the command install', fg='red'), err=True
        )
        sys.exit(1)
    click.echo('Downloading Rekono source code')
    download_source_code()                                                      # Download Rekono source code
    click.echo()
    click.echo('Updating Rekono dependencies')
    click.echo('[+] Rekono backend dependencies')
    install_backend()                                                           # Update backend dependencies
    click.echo('[+] Rekono frontend dependencies')
    install_frontend()                                                          # Update frontend dependencies
    click.echo()
    click.echo('Updating database')
    manage_command('migrate')                                                   # Migrate Rekono database
    click.echo()
    click.echo(click.style('Rekono has been updated!', fg='green'))


@click.command('uninstall', help='Uninstall Rekono from the system')
def uninstall():
    '''Uninstall Rekono from the system.'''
    check_system()                                                              # Check if it is a Linux system
    click.echo('Removing Rekono home directory')
    if os.path.isdir(REKONO_HOME_DIRECTORY):
        subprocess.run(['sudo', 'rm', '-R', REKONO_HOME_DIRECTORY, '-f'], capture_output=True)
    click.echo('Removing Rekono services')
    if check_rekono_installation():
        executors = count_running_services(f'rekono-{EXECUTIONS}')
        rekono_services_command('stop', executors)
    remove_rekono_user()
    remove_rekono_services()
    reload_systemctl()
    click.echo('Removing Rekono database')
    drop_rekono_database()
    click.echo()
    click.echo(click.style('Rekono has been uninstalled. Bye!', fg='green'))
