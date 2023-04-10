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
  <a href="https://www.buymeacoffee.com/pablosnt" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="75"/>
  </a>
</p>

# <p align="center"><img src="https://raw.githubusercontent.com/pablosnt/rekono/main/rekono/frontend/public/static/logo-black.png" width="500"/></p>

Command Line Interface to make requests to the [Rekono](https://github.com/pablosnt/rekono) API REST.


## Usage

<img width="507" alt="usage" src="https://user-images.githubusercontent.com/69458381/224380037-19638197-75dc-457c-b5aa-7dcc1f9d1a4d.png">

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


## Reach Us

You can get support, ask questions, solve doubts or solve problems using:

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

Rekono is an open source project that we really love to maintain and it's absolutely our pleasure, but we would like to offer the possibility of supporting Rekono's development via donations. At the moment, the project only needs its maintainer's time to stay up to date with new features and fix bugs. However, in the future, it could need more expensive resources like hosting, new web pages for documentation, the inclusion of premium hacking tools, etc. With the help received from our supporters, Rekono will be able to grow fastly and have the resources that it deserves. Of course, you can use the donations just to appreciate our work. Thank you for your help!

<a href="https://www.buymeacoffee.com/pablosnt" target="_blank">
  <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=pablosnt&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff"/>
</a>


## License

Rekono is licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](../LICENSE.md)
