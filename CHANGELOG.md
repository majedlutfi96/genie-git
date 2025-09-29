# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive unit test suite for all modules using `pytest`
- Continuous Integration (CI) pipeline using GitHub Actions to automatically lint and test code
- Test coverage reporting with Codecov
- Add context option for AI commit message suggestions
- Add `--copy` flag to copy commit messages to clipboard
- Add `--always-copy` and `--always-copy-off` configuration options for automatic clipboard copying

### Changed

- Refactored the CLI and main application logic into separate, more maintainable modules

### Fixed

- Handle empty git repositories gracefully

## [0.1.1] - 2025-09-16

### Added

-   MIT License file
-   Comprehensive CHANGELOG.md

### Changed

-   Enhanced README.md with detailed installation instructions, quick start guide, and usage examples
-   Improved project documentation structure

## [0.1.0] - 2025-09-15

### Added

-   Initial release of `genie-git`.
-   `suggest` command to generate commit messages from staged files.
-   `configure` command to set API key and model.
-   `exclude-files` command to ignore paths in the diff.
