<p align="center">
  <a href="https://github.com/pablosnt/rekono-cli/actions/workflows/security-sca.yml" alt="SCA">
    <img src="https://github.com/pablosnt/rekono-cli/actions/workflows/security-sca.yml/badge.svg"/>
  </a>
  <a href="https://github.com/pablosnt/rekono-cli/actions/workflows/security-secrets.yml" alt="Secrets scanning">
    <img src="https://github.com/pablosnt/rekono-cli/actions/workflows/security-secrets.yml/badge.svg"/>
  </a>
  <a href="https://github.com/pablosnt/rekono-cli/actions/workflows/code-style.yml" alt="Code style">
    <img src="https://github.com/pablosnt/rekono-cli/actions/workflows/code-style.yml/badge.svg"/>
  </a>
</p>

# <p align="center"><img src="assets/logo-black.png" width="500"/></p>

This is a Command Line Interface to manage the [Rekono](https://github.com/pablosnt/rekono) environment.


## Usage

|Command|Description|
|-------|-----------|
|`install`|Install Rekono in the system|
|`install --all-tools`|Install Rekono and all supported tools|
|`update`|Update Rekono to the last version|
|`uninstall`|Uninstall Rekono from your system|
|`services start --execution-workers <N>`|Start all Rekono services with N executions workers (3 by default)|
|`services stop`|Stop all Rekono services|
|`services restart`|Restart all Rekono services|

> :warning: Only tested in Kali Linux.  

> :warning: Only use that to manage Rekono environment for local and personal usage. Otherwise [Docker](https://github.com/pablosnt/rekono#docker) is advised.  


## Installation

### PIP

```
pip3 install rekono-cli
```

### From Source

1. Install the required technologies:
    - Python 3 & PIP

2. Install the dependencies:

    ```
    pip3 install -r requirements.txt
    ```

3. Execute the CLI:

    ```
    python3 rekono/main.py --help
    ```


## Configuration

By default Rekono will be installed in `/opt/rekono`. You can change this directory using the environment variable `REKONO_HOME`.

Check the [Rekono configuration](https://github.com/pablosnt/rekono) for more information.


## License

Rekono is licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](./LICENSE.md)