# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2023-05-07

### Added

- [**BREAKING**] Remove `install`, `update`, `uninstall` and `services` commands (https://github.com/pablosnt/rekono-cli/issues/34)
- [**BREAKING**] Remove support for Rekono basic authentication (https://github.com/pablosnt/rekono-cli/issues/38)
- [**BREAKING**] Change `rekono` command by `rekono-cli` command (https://github.com/pablosnt/rekono-cli/issues/46)
- Optimize, improve, clean and test source code (https://github.com/pablosnt/rekono-cli/issues/36)
- Specific commands to manage specific Rekono entities (https://github.com/pablosnt/rekono-cli/issues/40)


## [1.1.0] - 2023-01-11

### Added

- Add `Nuclei` installation (https://github.com/pablosnt/rekono-cli/pull/19)
- Add `Spring4Shell Scan` installation (https://github.com/pablosnt/rekono-cli/pull/20)
- Add `Log4j Scan` installation (https://github.com/pablosnt/rekono-cli/pull/21)
- Add `Gobuster` installation (https://github.com/pablosnt/rekono-cli/pull/24)
- Add `--version` option to check current Rekono CLI version (https://github.com/pablosnt/rekono-cli/pull/31)

### Changed

- Remove installation of `wordlists` package (https://github.com/pablosnt/rekono-cli/pull/23)
- Upgrade `requests` to version `2.28.1` (https://github.com/pablosnt/rekono-cli/pull/27)


## [1.0.3] - 2022-11-01

### Changed

- Remove configuration properties that are included in the new Rekono `Settings` page (https://github.com/pablosnt/rekono-cli/pull/11)


## [1.0.2] - 2022-10-07

### Fixed

- Error during installation via PIP due to the lack of the `NODE_OPTIONS` environment variable (https://github.com/pablosnt/rekono-cli/pull/8)


## [1.0.1] - 2022-09-03

### Fixed

- Error during installation via PIP because `requirements.txt` is not found (https://github.com/pablosnt/rekono-cli/pull/6)


## [1.0.0] - 2022-08-19

### Added

- Make `Rekono API` requests
- `Install` Rekono in the system
- `Update` Rekono to the last version
- `Uninstall` Rekono from the system
- `Start` all Rekono services using systemctl
- `Stop` all Rekono services using systemctl
- `Restart` all Rekono services using systemctl