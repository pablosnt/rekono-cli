import os
import shutil
import subprocess
import sys

from git import Repo

from rekono.config import GITTOOLS_DIR, LOG4J_SCANNER_DIR
from rekono.utils.linux.apt import apt_install


def install_tools() -> None:
    '''Install all tools supported by Rekono.'''
    apt_install(
        [
            'nmap', 'dirsearch', 'theharvester', 'nikto', 'sslscan', 'sslyze',
            'cmseek', 'zaproxy', 'exploitdb', 'metasploit-framework',
            'emailharvester', 'joomscan', 'gitleaks', 'smbmap'
        ],
        required=False
    )
    subprocess.run([
        'sudo', sys.executable, '-m', 'pip', 'install', '-q', 'emailfinder', 'ssh-audit'
    ])
    for git_repository, directory in [
        ('https://github.com/cisagov/log4j-scanner.git', LOG4J_SCANNER_DIR),
        ('https://github.com/internetwache/GitTools.git', GITTOOLS_DIR),
    ]:
        if not os.path.isdir(directory):
            subprocess.run(['sudo', 'mkdir', directory])                        # Create tool directory
            subprocess.run(['sudo', 'chmod', '-R', '777', directory])           # Change tool directory permissions
            Repo.clone_from(git_repository, directory)
    log4j_scanner_req = os.path.join(LOG4J_SCANNER_DIR, 'log4-scanner', 'requirements.txt')
    if os.path.isfile(log4j_scanner_req):
        subprocess.run([                                                        # Install dependencies for Log4J Scanner
            'sudo', sys.executable, '-m', 'pip', 'install', '-q', '-r', log4j_scanner_req
        ])


def configure_tools() -> None:
    '''Configure all tools supported by Rekono.'''
    nmap = shutil.which('nmap')
    if nmap:
        # Set capabilities to nmap
        subprocess.run(['sudo', 'setcap', 'cap_net_raw,cap_net_admin,cap_net_bind_service+eip', nmap])


def install_resources() -> None:
    '''Install all resources used by Rekono.'''
    apt_install(['wordlists', 'seclists', 'dirb'])
    rockyou = '/usr/share/wordlists/rockyou.txt'
    if os.path.isfile(f'{rockyou}.gz') and not os.path.isfile(rockyou):
        subprocess.run(['sudo', 'gzip', '-d', f'{rockyou}.gz'], capture_output=True)    # Decompress rockyou wordlist
