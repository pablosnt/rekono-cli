<p align="center">
  <a href="https://snyk.io/test/github/pablosnt/rekono-cli" alt="SCA">
    <img src="https://badgen.net/snyk/pablosnt/rekono-cli?label=Vulnerabilities&labelColor=black&icon=https://snyk.io/wp-content/uploads/patch-white.svg">
  </a>
  <a href="https://github.com/pablosnt/rekono-cli/actions/workflows/security-secrets.yml" alt="Secrets scanning">
    <img src="https://github.com/pablosnt/rekono-cli/actions/workflows/security-secrets.yml/badge.svg"/>
  </a>
  <a href="https://github.com/pablosnt/rekono-cli/actions/workflows/code-style.yml" alt="Code style">
    <img src="https://github.com/pablosnt/rekono-cli/actions/workflows/code-style.yml/badge.svg"/>
  </a>
  <a href="https://discord.gg/Zyduu5C7M3">
    <img src="https://img.shields.io/badge/Discord-Join-black?style=social&logo=discord"/>
  </a>
</p>

# <p align="center"><img src="assets/logo-black.png" width="500"/></p>

This is a Command Line Interface to manage the [Rekono](https://github.com/pablosnt/rekono) platform:

- Make HTTP requests to the Rekono API REST
- Installation of Rekono in personal Linux environments
- Management of the Rekono services in personal Linux environments


## Usage

|Command|Description|
|-------|-----------|
|`api delete <endpoint>`|HTTP DELETE request to Rekono API|
|`api get <endpoint> --parameter <key>=<value>`|HTTP GET request to Rekono API|
|`api post <endpoint> --data <data>`|HTTP POST request to Rekono API|
|`api put <endpoint> --data <data>`|HTTP PUT request to Rekono API|
|`install`|Install Rekono in the system|
|`install --all-tools`|Install Rekono and all supported tools|
|`update`|Update Rekono to the last version|
|`uninstall`|Uninstall Rekono from your system|
|`services start --execution-workers <N>`|Start all Rekono services with N executions workers (3 by default)|
|`services stop`|Stop all Rekono services|
|`services restart`|Restart all Rekono services|

> :warning: Commands to manage Rekono installation are only advised for local and personal usage in Linux environements. Otherwise [Docker](https://github.com/pablosnt/rekono#docker) is advised.

You can reach Rekono in http://127.0.0.1:3000/

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

You can use the following environment variables to configure the Rekono CLI:

- `REKONO_HOME`: Directory for Rekono installation. By default, Rekono will be installed in `/opt/rekono`
- `REKONO_URL`: Rekono URL in format `<schema>://<host>` to be used in API requests
- `REKONO_TOKEN`: API token for Rekono API authentication

Check the [Rekono configuration](https://github.com/pablosnt/rekono/wiki/Configuration) for more information.


## Support

You can reach us on:

<p>
  <a href="https://github.com/pablosnt/rekono-cli/issues/new?labels=help+wanted%2C+question&template=support.md" alt="GitHub Issue">
    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="64"/>
  </a>
  <a href="https://discord.gg/Zyduu5C7M3" alt="Discord">
    <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a69f118df70ad7828d4_icon_clyde_blurple_RGB.svg" width="64"/>
  </a>
</p>

If you need more specific help, you can also mail rekono.project@gmail.com.


## License

Rekono is licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](./LICENSE.md)