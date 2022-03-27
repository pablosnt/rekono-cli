import shutil


def check_installation(executable: str) -> bool:
    '''Check if executable is installed or not.

    Args:
        executable (str): Executable to check

    Returns:
        bool: Indicate if executable is installed or not
    '''
    return shutil.which(executable) is not None
