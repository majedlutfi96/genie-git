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
        always_copy=False,
        always_copy_off=False,
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
    args = Namespace(
        show=True,
        model=None,
        api_key=None,
        message_specifications=None,
        always_copy=False,
        always_copy_off=False,
    )
    handle_configure(args)
    mock_config_instance.show.assert_called_once()


def test_handle_configure_with_always_copy(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_configure sets always_copy to True."""
    args = Namespace(
        model=None,
        api_key=None,
        message_specifications=None,
        show=False,
        always_copy=True,
        always_copy_off=False,
    )

    handle_configure(args)

    assert mock_config_instance.always_copy is True
    mock_config_instance.save.assert_called_once()


def test_handle_configure_with_always_copy_off(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_configure sets always_copy to False."""
    args = Namespace(
        model=None,
        api_key=None,
        message_specifications=None,
        show=False,
        always_copy=False,
        always_copy_off=True,
    )

    handle_configure(args)

    assert mock_config_instance.always_copy is False
    mock_config_instance.save.assert_called_once()


def test_handle_configure_with_conflicting_copy_flags(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_configure raises Error when both copy flags are provided."""
    args = Namespace(
        model=None,
        api_key=None,
        message_specifications=None,
        show=False,
        always_copy=True,
        always_copy_off=True,
    )

    with pytest.raises(
        ValueError, match="--always-copy and --always-copy-off cannot be used together."
    ):
        handle_configure(args)


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
    mock_pyperclip = mocker.patch("genie_git.cli_handlers.pyperclip")

    # Set always_copy to False by default
    mock_config_instance.always_copy = False

    handle_suggest(Namespace(context="test_context", copy=False))

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

    # Should not copy to clipboard when both always_copy and copy are False
    mock_pyperclip.copy.assert_not_called()


def test_handle_suggest_with_copy_flag(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_suggest copies to clipboard when --copy flag is used."""
    mocker.patch("genie_git.cli_handlers.get_log", return_value="test_log")
    mocker.patch(
        "genie_git.cli_handlers.get_repository_changes", return_value="test_changes"
    )
    mocker.patch(
        "genie_git.cli_handlers.suggest_commit_message", return_value="test_message"
    )
    mock_pyperclip = mocker.patch("genie_git.cli_handlers.pyperclip")

    # Set always_copy to False
    mock_config_instance.always_copy = False

    handle_suggest(Namespace(context="test_context", copy=True))

    # Should copy to clipboard when copy flag is True
    mock_pyperclip.copy.assert_called_once_with("test_message")


def test_handle_suggest_with_always_copy_config(
    mock_config_instance: MagicMock, mocker: MockerFixture
) -> None:
    """Test that handle_suggest copies to clipboard when always_copy is configured."""
    mocker.patch("genie_git.cli_handlers.get_log", return_value="test_log")
    mocker.patch(
        "genie_git.cli_handlers.get_repository_changes", return_value="test_changes"
    )
    mocker.patch(
        "genie_git.cli_handlers.suggest_commit_message", return_value="test_message"
    )
    mock_pyperclip = mocker.patch("genie_git.cli_handlers.pyperclip")

    # Set always_copy to True
    mock_config_instance.always_copy = True

    handle_suggest(Namespace(context="test_context", copy=False))

    # Should copy to clipboard when always_copy is True
    mock_pyperclip.copy.assert_called_once_with("test_message")


def test_handle_suggest_with_no_staged_changes(mocker: MockerFixture) -> None:
    """Test that handle_suggest handles empty staged changes gracefully."""
    mocker.patch("genie_git.cli_handlers.get_repository_changes", return_value="")
    mock_print = mocker.patch("builtins.print")

    handle_suggest(Namespace(context="test_context", copy=False))
    mock_print.assert_called_once_with("No staged changes found in the repository.")


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


def test_handle_exclude_files_with_non_existing_files(mocker: MockerFixture) -> None:
    """Test that handle_exclude_files raises an error when files do not exist."""
    mocker.patch("genie_git.cli_handlers.Path.exists", return_value=False)

    with pytest.raises(FileNotFoundError, match="File test_file1 does not exist."):
        handle_exclude_files(Namespace(files=["test_file1", "test_file2"]))
