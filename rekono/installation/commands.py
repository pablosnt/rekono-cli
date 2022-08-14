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
from rekono.services.commands import restart, start, stop
from rekono.services.manager import (create_rekono_services,
                                     remove_rekono_services)
from rekono.utils.linux.apt import apt_install, apt_update
from rekono.utils.linux.check import check_system
from rekono.utils.linux.systemctl import (count_running_services,
                                          reload_systemctl, systemctl_command)
from rekono.utils.linux.users import create_rekono_user, remove_rekono_user
from rekono.utils.source_code import download_source_code


@click.command('install', help='Install Rekono on the system')
@click.option(
    '-a', '--all-tools', 'all_tools', is_flag=True,
    help='Install all tools and resources supported by Rekono'
)
@click.pass_context
def install(ctx: click.Context, all_tools: bool):
    '''Install Rekono on the system.

    Args:
        ctx (click.Context): Click context to be able to call other Click commands
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
    create_rekono_user()                                                        # Create Rekono system user
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
        install_tools()                                                         # Install all supported tools
        configure_tools()                                                       # Configure supported tools
        click.echo('Installing all supported resources')
        install_resources()                                                     # Install resources by default
    click.echo()
    click.echo('Creating systemd services for Rekono')
    create_rekono_services()                                                    # Create Rekono services
    reload_systemctl()                                                          # Reload Systemctl daemon
    click.echo()
    click.echo(click.style('Installation completed!', fg='green'))
    click.echo()
    answer = input('Do you want to start Rekono services? [Y/N]: ')
    if answer.lower() in ['y', 'yes']:
        answer = input('How many execution workers do you need? [3]: ')
        try:
            execution_workers = int(answer)
        except ValueError:
            execution_workers = 3
        ctx.invoke(start, executors=execution_workers)                          # Start Rekono services


@click.command('update', help='Update Rekono installation with the latest version')
@click.pass_context
def update(ctx: click.Context):
    '''Update Rekono installation with the latest version.

    Args:
        ctx (click.Context): Click context to be able to call other Click commands
    '''
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
    manage_command('frontend')                                                  # Configure Rekono frontend
    click.echo()
    click.echo('Updating database')
    systemctl_command('start', 'postgresql')                                    # Start PostgreSQL
    manage_command('migrate')                                                   # Migrate Rekono database
    click.echo()
    if count_running_services('rekono-') > 0:
        click.echo('Restarting services')
        ctx.invoke(restart)                                                     # Restart Rekono services
        click.echo()
    click.echo(click.style('Rekono has been updated!', fg='green'))


@click.command('uninstall', help='Uninstall Rekono from the system')
@click.pass_context
def uninstall(ctx: click.Context):
    '''Uninstall Rekono from the system.

    Args:
        ctx (click.Context): Click context to be able to call other Click commands
    '''
    check_system()                                                              # Check if it is a Linux system
    if check_rekono_installation():
        click.echo('Stopping Rekono services')
        ctx.invoke(stop)                                                        # Stop Rekono services
    click.echo('Removing Rekono services')
    remove_rekono_user()                                                        # Remove Rekono user
    remove_rekono_services()                                                    # Remove Rekono systemctl services
    reload_systemctl()                                                          # Reload systemctl daemon
    click.echo('Removing Rekono home directory')
    if os.path.isdir(REKONO_HOME_DIRECTORY):
        subprocess.run(['sudo', 'rm', '-R', REKONO_HOME_DIRECTORY, '-f'], capture_output=True)
    click.echo('Removing Rekono database')
    drop_rekono_database()                                                      # Remove Rekono database
    click.echo()
    click.echo(click.style('Rekono has been uninstalled. Bye!', fg='green'))
