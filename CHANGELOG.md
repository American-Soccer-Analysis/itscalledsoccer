# Changelog

All notable changes to `itscalledsoccer` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

Changes are grouped by type: `Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, and `Security`.

## [Unreleased]

### Changed

- Ongoing maintenance and dependency updates since `v2.1.0`.

## [2.1.0] - 2026-05-13

### Added

- Custom exception classes for invalid parameters, leagues, seasons, and entity types.

### Fixed

- Game sorting when results include older data.

## [2.0.0] - 2026-05-12

### Added

- Expanded API examples and documentation.
- Retry handling and configurable request timeouts.
- Instance-specific logging.

### Fixed

- Entity name lookup lazy loading.
- Game query season parameter consistency.
- Empty game result handling.
- Entity URL construction and type handling.

## [1.3.6] - 2026-04-27

### Fixed

- Fixed lazy loading, fragile keyword handling, and entity name conversion.
- Cleaned up legacy type hints and DataFrame references.

## [1.3.5] - 2026-04-10

### Fixed

- Improved error handling, default DataFrame initialization, CI setup, and
  documentation.

### Changed

- Updated the lockfile and development tooling.

## [1.3.4] - 2026-02-03

### Changed

- Dropped Python 3.9 support.
- Grouped dependency updates and refreshed security tooling.

## [1.3.3] - 2025-06-07

### Added

- Added the `status` keyword to `get_games`.

### Changed

- Updated CI, CodeQL, dependency review, Codecov, and Scorecard workflows.

## [1.3.2] - 2025-02-18

### Fixed

- Fixed boolean defaults and the `get_team_salaries` default behavior.

## [1.3.1] - 2024-12-13

### Added

- Added OpenSSF Scorecard checks, dependency automation, a development
  container, and PyPI attestations.

### Changed

- Applied security hardening and reorganized the README.

## [1.3.0] - 2024-08-29

### Added

- Added USL Super League support and project documentation.
- Added local coverage reporting and Codecov integration.

### Changed

- Switched project management to `uv`, testing to pytest, and documentation to
  Google-style docstrings.

## [1.2.1] - 2024-06-27

### Fixed

- Corrected the stadium endpoint and improved Windows test compatibility.

## [1.2.0] - 2024-06-21

### Added

- Added lazy loading for entity data and the project documentation site.

### Changed

- Switched to pytest, Google-style docstrings, PyPI trusted publishing, and
  the `pyproject.toml` project configuration.

## [1.1.0] - 2023-08-13

### Added

- Added manual cache clearing and download statistics.

### Changed

- Updated dependency management and the PyPI build workflow.

## [1.0.0] - 2023-05-22

### Added

- Added Python 3.10 and 3.11 testing, Dependabot, CODEOWNERS, and expanded
  test fixtures.

### Changed

- Established the 1.0 API release and updated dependencies and packaging.

## [0.2.0] - 2022-04-13

### Added

- Added MLS Next Pro (`mlsnp`) as a supported league.

### Fixed

- Improved handling of API null values, request parameters, and CI tooling.

## [0.1.4] - 2022-02-25

### Fixed

- Improved query caching and pagination behavior.

## [0.1.3] - 2022-02-22

### Fixed

- Corrected conversion of list parameters before API requests.

## [0.1.2] - 2022-02-17

### Added

- Added dependency declarations and issue templates.

## [0.1.1] - 2022-02-09

### Fixed

- Corrected package discovery and PyPI publishing configuration.

## [0.1.0] - 2022-02-08

### Added

- Initial Python package release.
- Added entity, game, advanced statistics, salary, proxy, and configurable
  logging APIs.
- Added tests, type checking, formatting, and CI workflows.

[Unreleased]: https://github.com/American-Soccer-Analysis/itscalledsoccer/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v2.1.0
[2.0.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v2.0.0
[1.3.6]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.6
[1.3.5]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.5
[1.3.4]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.4
[1.3.3]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.3
[1.3.2]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.2
[1.3.1]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.1
[1.3.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.3.0
[1.2.1]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.2.1
[1.2.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.2.0
[1.1.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.1.0
[1.0.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v1.0.0
[0.2.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v0.2.0
[0.1.4]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v0.1.4
[0.1.3]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v0.1.3
[0.1.2]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v0.1.2
[0.1.1]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v0.1.1
[0.1.0]: https://github.com/American-Soccer-Analysis/itscalledsoccer/releases/tag/v0.1.0
