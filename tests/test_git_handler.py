"""Test the git handler module."""

from pytest_mock import MockerFixture

from genie_git.git_handler import get_log, get_repository_changes


def test_get_log(mocker: MockerFixture) -> None:
    """Test get_log returns the correct log."""
    mock_repo_instance = mocker.MagicMock()
    mock_repo_instance.git.log.return_value = "test_log"

    mocker.patch("genie_git.git_handler.git.Repo", return_value=mock_repo_instance)

    assert get_log(7) == "test_log"
    mock_repo_instance.git.log.assert_called_once_with("-7", "--pretty=format:%s")


def test_get_repository_changes_with_no_exclusions(mocker: MockerFixture) -> None:
    """Test get_repository_changes calls 'git diff' correctly with no exclusions."""
    mock_repo_instance = mocker.MagicMock()
    mocker.patch("genie_git.git_handler.git.Repo", return_value=mock_repo_instance)

    get_repository_changes()

    mock_repo_instance.git.diff.assert_called_once_with("--staged")


def test_get_repository_changes_with_exclusions(mocker: MockerFixture) -> None:
    """Test get_repository_changes calls 'git diff' correctly with exclusions."""
    mock_repo_instance = mocker.MagicMock()
    mocker.patch("genie_git.git_handler.git.Repo", return_value=mock_repo_instance)

    get_repository_changes(exclude_files=["test_file", "test_file2"])

    mock_repo_instance.git.diff.assert_called_once_with(
        "--staged", ":(exclude)test_file :(exclude)test_file2"
    )
