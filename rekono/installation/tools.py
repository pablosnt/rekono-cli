import os
import shutil
import subprocess
import sys

from git import Repo
from rekono.config import GITTOOLS_DIR, LOG4J_SCAN_DIR, SPRING4SHELL_SCAN_DIR
from rekono.utils.linux.apt import apt_install


def install_tools() -> None:
    '''Install all tools supported by Rekono.'''
    apt_install(
        [
            'nmap', 'dirsearch', 'theharvester', 'nikto', 'sslscan', 'sslyze',
            'cmseek', 'zaproxy', 'exploitdb', 'metasploit-framework',
            'emailharvester', 'joomscan', 'gitleaks', 'smbmap', 'nuclei',
            'gobuster'
        ],
        required=False
    )
    subprocess.run([
        'sudo', sys.executable, '-m', 'pip', 'install', '-q', 'emailfinder', 'ssh-audit'
    ])
    for git_repository, directory in [
        ('https://github.com/fullhunt/log4j-scan', LOG4J_SCAN_DIR),
        ('https://github.com/fullhunt/spring4shell-scan.git', SPRING4SHELL_SCAN_DIR),
        ('https://github.com/internetwache/GitTools.git', GITTOOLS_DIR),
    ]:
        if not os.path.isdir(directory):
            subprocess.run(['sudo', 'mkdir', directory])                        # Create tool directory
            subprocess.run(['sudo', 'chmod', '-R', '777', directory])           # Change tool directory permissions
            Repo.clone_from(git_repository, directory)
    for requirements in [
        os.path.join(LOG4J_SCAN_DIR, 'requirements.txt'),
        os.path.join(SPRING4SHELL_SCAN_DIR, 'requirements.txt'),
    ]:
        if os.path.isfile(requirements):
            subprocess.run([                                                    # Install Python dependencies
                'sudo', sys.executable, '-m', 'pip', 'install', '-q', '-r', requirements
            ])


def configure_tools() -> None:
    '''Configure all tools supported by Rekono.'''
    nmap = shutil.which('nmap')
    if nmap:
        # Set capabilities to nmap
        subprocess.run(['sudo', 'setcap', 'cap_net_raw,cap_net_admin,cap_net_bind_service+eip', nmap])


def install_resources() -> None:
    '''Install all resources used by Rekono.'''
    apt_install(['seclists', 'dirb'])
