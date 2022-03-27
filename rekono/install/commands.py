import platform
import sys

import click
from install.dependencies import (install_backend, install_frontend,
                                  install_postgresql, install_rq, install_vue)
from install.initialization import create_config_file, manage_command
from services.manager import create_rekono_services
from utils.linux.apt import apt_install, apt_update
from utils.linux.systemctl import reload_systemctl
from utils.source_code.rekono import download_source_code


@click.command('install', help='Install Rekono in the system')
def install():
    '''Install Rekono in the system.'''
    if platform.system().lower() == 'linux':
        # Local installation is only available for Linux
        click.echo('Downloading Rekono source code')
        download_source_code()                                                  # Download Rekono source code
        click.echo()
        click.echo('Installing Rekono dependencies')
        apt_update()                                                            # Update APT sources
        click.echo('[+] PostgreSQL')
        db_password = install_postgresql()                                      # Install PostgreSQL
        click.echo('[+] Redis')
        install_rq()                                                            # Install Redis Queue
        click.echo('[+] Vue')
        install_vue()                                                           # Install Vue
        click.echo('[+] Other packages')
        apt_install(['libpq-dev', 'python3-dev'])                               # Install other dependencies
        click.echo('[+] Rekono backend dependencies')
        install_backend()                                                       # Install backend dependencies
        click.echo('[+] Rekono frontend dependencies')
        install_frontend()                                                      # Install frontend dependencies
        click.echo()
        click.echo('Configuring Rekono')
        click.echo("Don't worry if you can't configure some items, press ENTER")
        create_config_file(db_password)                                         # Create Rekono configuration
        click.echo()
        manage_command('migrate')                                               # Migrate Rekono database
        click.echo()
        click.echo('Creation first Rekono user')
        manage_command('createsuperuser')                                       # Create Rekono superuser
        manage_command('frontend')                                              # Configure Rekono frontend
        click.echo()
        click.echo('Creating systemd services for Rekono')
        create_rekono_services()
        reload_systemctl()
        click.echo()
        click.echo(click.style('Installation completed!', fg='green'))
    else:
        click.echo(click.style('Installation only works in Linux systems', fg='red'), err=True)
        click.echo('For this system, you can follow this steps to deploy Rekono in Docker: ')
        sys.exit(1)
