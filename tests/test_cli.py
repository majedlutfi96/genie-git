"""Test the CLI commands."""

from argparse import Namespace

import pytest
from pytest_mock import MockerFixture

from genie_git.main import handle_configure, handle_exclude_files, handle_suggest


def test_handle_configure(mocker: MockerFixture) -> None:
    """Tests that handle_configure updates the configurations file."""
    mock_config_instance = mocker.MagicMock()
    mocker.patch("genie_git.main.Config.load", return_value=mock_config_instance)

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

    args.show = True
    handle_configure(args)
    mock_config_instance.show.assert_called_once()


def test_handle_suggest(mocker: MockerFixture) -> None:
    """Tests that handle_suggest calls all it's dependencies."""
    mock_config_instance = mocker.MagicMock()
    mocker.patch("genie_git.main.Config.load", return_value=mock_config_instance)

    mock_get_log = mocker.patch("genie_git.main.get_log", return_value="test_log")
    mock_get_repository_changes = mocker.patch(
        "genie_git.main.get_repository_changes", return_value="test_changes"
    )
    mock_suggest_commit_message = mocker.patch(
        "genie_git.main.suggest_commit_message", return_value="test_message"
    )

    handle_suggest(Namespace())

    mock_get_repository_changes.assert_called_once_with(
        mock_config_instance.exclude_files
    )

    mock_get_log.assert_called_once_with(mock_config_instance.number_of_commits)

    mock_suggest_commit_message.assert_called_once_with(
        api_key=mock_config_instance.api_key,
        git_logs="test_log",
        staged_changes="test_changes",
        message_specifications=mock_config_instance.message_specifications,
    )


def test_handle_exclude_files(mocker: MockerFixture) -> None:
    """Tests that handle_exclude_files updates the configurations file."""
    mock_config_instance = mocker.MagicMock()
    mocker.patch("genie_git.main.Config.load", return_value=mock_config_instance)

    # testing with valid files
    mocker.patch("genie_git.main.Path.exists", return_value=True)
    handle_exclude_files(Namespace(files=["test_file1", "test_file2"]))

    assert mock_config_instance.exclude_files.extend.is_called_once_with(
        ["test_file1", "test_file2"]
    )

    assert mock_config_instance.save.is_called_once()

    # testing with non existing files
    mocker.patch("genie_git.main.Path.exists", return_value=False)

    with pytest.raises(FileNotFoundError, match="File test_file1 does not exist."):
        handle_exclude_files(Namespace(files=["test_file1", "test_file2"]))
