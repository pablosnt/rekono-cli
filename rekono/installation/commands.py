import os
import sys

import click
from config import REKONO_HOME_DIRECTORY
from installation.check import check_rekono_installation
from installation.dependencies import (install_backend, install_frontend,
                                       install_postgresql, install_rq,
                                       install_vue)
from installation.initialization import create_config_file, manage_command
from services.manager import create_rekono_services
from utils.linux.apt import apt_install, apt_update
from utils.linux.check import check_system
from utils.linux.systemctl import reload_systemctl
from utils.source_code.rekono import download_source_code


@click.command('install', help='Install Rekono on the system')
def install():
    '''Install Rekono on the system.'''
    check_system()                                                              # Check if it is a Linux system
    if check_rekono_installation():
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
    click.echo()
    click.echo('Creating systemd services for Rekono')
    create_rekono_services()
    reload_systemctl()
    click.echo()
    click.echo(click.style('Installation completed!', fg='green'))


@click.command('update', help='Update Rekono installation with the latest version')
def update():
    '''Update Rekono installation with the latest version.'''
    check_system()                                                              # Check if it is a Linux system
    if not check_rekono_installation():
        click.echo(
            click.style('Rekono is not installed on the system. Please, run the command install', fg='red'), err=True
        )
        sys.exit(1)
    click.echo('Downloading Rekono source code')
    download_source_code()                                                      # Download Rekono source code
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
