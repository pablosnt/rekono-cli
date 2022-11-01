# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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