"""Test the CLI commands."""

from argparse import Namespace
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from genie_git.cli_handlers import (
    handle_configure,
    handle_exclude_files,
    handle_suggest,
)


def test_handle_configure(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_configure updates the configurations file."""
    args = Namespace(
        model="test_model",
        api_key="test_api_key",
        message_specifications="test_message_specifications",
        show=False,
    )

    handle_configure(args)

    mock_config_instance.save.assert_called_once()

    assert mock_config_instance.model == "test_model"
    assert mock_config_instance.api_key == "test_api_key"
    assert mock_config_instance.message_specifications == "test_message_specifications"

    mock_config_instance.show.assert_not_called()


def test_handle_configure_with_show(
    mock_config_instance: MagicMock, mocker: MockerFixture
):
    """Test that handle_configure shows the configurations file."""
    args = Namespace(show=True, model=None, api_key=None, message_specifications=None)
    args.show = True
    handle_configure(args)
    mock_config_instance.show.assert_called_once()


def test_handle_suggest(mock_config_instance: MagicMock, mocker: MockerFixture) -> None:
    """Test that handle_suggest calls all it's dependencies."""
    mock_get_log = mocker.patch(
        "genie_git.cli_handlers.get_log", return_value="test_log"
    )
    mock_get_repository_changes = mocker.patch(
        "genie_git.cli_handlers.get_repository_changes", return_value="test_changes"
    )
    mock_suggest_commit_message = mocker.patch(
        "genie_git.cli_handlers.suggest_commit_message", return_value="test_message"
    )

    handle_suggest(Namespace(context="test_context"))

    mock_get_repository_changes.assert_called_once_with(
        mock_config_instance.exclude_files
    )

    mock_get_log.assert_called_once_with(mock_config_instance.number_of_commits)

    mock_suggest_commit_message.assert_called_once_with(
        api_key=mock_config_instance.api_key,
        git_logs="test_log",
        staged_changes="test_changes",
        message_specifications=mock_config_instance.message_specifications,
        context="test_context",
    )


def test_handle_exclude_files(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_exclude_files updates the configurations file."""
    mocker.patch("genie_git.cli_handlers.Path.exists", return_value=True)
    handle_exclude_files(Namespace(files=["test_file1", "test_file2"]))

    mock_config_instance.exclude_files.extend.assert_called_once_with(
        ["test_file1", "test_file2"]
    )

    mock_config_instance.save.assert_called_once()


def test_handle_exclude_files_with_non_existing_files(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_exclude_files raises an error when a file does not exist."""
    mocker.patch("genie_git.cli_handlers.Path.exists", return_value=False)

    with pytest.raises(FileNotFoundError, match="File test_file1 does not exist."):
        handle_exclude_files(Namespace(files=["test_file1", "test_file2"]))
