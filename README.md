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

# <p align="center"><img src="https://raw.githubusercontent.com/pablosnt/rekono/main/rekono/frontend/public/static/logo-black.png" width="500"/></p>

Command Line Interface to make requests to the [Rekono](https://github.com/pablosnt/rekono) API REST.


## Usage

# TODO: IMAGE

> Rekono API documentation is available in `/api/schema/swagger-ui.html` and `/api/schema/redoc/` of Rekono instances

## Library usage

Rekono CLI can be also used as Python 3 library, so that it's possible to create custom Rekono scripts. For example, with the following code it's possible to create a Rekono client to make custom API requests:

```python
from rekono.client.api import Rekono
client = Rekono(url='https://127.0.0.1', token='my secret api token')           # Create Rekono client
response = client.get('/api/tools/1/')                                          # GET request to get tool with ID 1
```


## Installation

### PIP

```bash
pip3 install rekono-cli
```

### From Source

1. Install the required technologies:
    - Python 3 & PIP

2. Install the dependencies:

    ```bash
    pip3 install -r src/requirements.txt
    ```

3. Execute the CLI:

    ```bash
    python3 src/rekono/main.py --help
    ```


## Configuration

You can use the `REKONO_TOKEN` environment variable to configure the API token for Rekono authentication.


## Support

<p>
  <a href="https://github.com/pablosnt/rekono/issues/new?labels=help+wanted%2C+question&template=support.md" alt="GitHub Issue">
    <img src="https://github.com/fluidicon.png" width="64"/>
  </a>
  <a href="https://discord.gg/Zyduu5C7M3" alt="Discord">
    <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a69f118df70ad7828d4_icon_clyde_blurple_RGB.svg" width="64"/>
  </a>
  <a href="mailto:rekono.project@gmail.com" alt="Mail">
    <img src="https://www.gstatic.com/images/branding/product/2x/gmail_2020q4_512dp.png" width="64"/>
  </a>
</p>


## License

Rekono is licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](../LICENSE.md)