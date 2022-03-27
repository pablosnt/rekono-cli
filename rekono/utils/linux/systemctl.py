import subprocess


def reload_systemctl() -> None:
    '''Reload systemctl daemon.'''
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'], capture_output=True)


def systemctl_command(command: str, service: str) -> None:
    '''Execute systemctl command to one service.

    Args:
        command (str): Systemctl command
        service (str): Systemctl service
    '''
    subprocess.run(['sudo', 'systemctl', command, service], capture_output=True)


def count_running_services(service: str) -> int:
    '''Count number of running executions for one service at the moment.

    Args:
        service (str): Systemctl service to count his executions

    Returns:
        int: Number of running executions
    '''
    exec = subprocess.run(['sudo', 'systemctl', 'list-units', '--type=service', '--state=running'], capture_output=True)
    count = 0
    if exec.returncode == 0 and exec.stdout:
        services = [line.strip() for line in exec.stdout.decode().split('\n') if line.strip().startswith(service)]
        count = len(services)
    return count
