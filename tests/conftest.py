"""Conftest file for pytest."""

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_config_instance(mocker: MockerFixture) -> MagicMock:
    """Mock the Config instance."""
    mock_instance = mocker.MagicMock()
    mocker.patch("genie_git.cli_handlers.Config.load", return_value=mock_instance)
    return mock_instance
