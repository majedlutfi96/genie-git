"""Test the config module."""

from pathlib import Path

from pytest_mock import MockerFixture

from genie_git.config import Config


def test_config_save_and_load(tmp_path: Path, mocker: MockerFixture) -> None:
    """Tests that a config object can be saved and loaded."""
    config_file = tmp_path / "config.json"

    mocker.patch("genie_git.config.CONFIG_FILE", config_file)

    new_config = Config(
        api_key="testing-key",
        model="testing-model",
        exclude_files=["testing-file"],
        number_of_commits=10,
        message_specifications="testing-specifications",
    )

    new_config.save()

    loaded_config = Config.load()

    assert loaded_config.api_key == "testing-key"
    assert loaded_config.model == "testing-model"
    assert loaded_config.exclude_files == ["testing-file"]
    assert loaded_config.number_of_commits == 10
    assert loaded_config.message_specifications == "testing-specifications"

    assert config_file.exists()


def test_config_load_without_existing_file(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    """Tests that Config.load() returns a default Config when file does not exist."""
    mocker.patch("genie_git.config.CONFIG_FILE", tmp_path / "no_config.json")

    loaded_config = Config.load()

    assert loaded_config.api_key == ""
    assert loaded_config.model == "gemini-2.5-flash"
    assert loaded_config.exclude_files == []
    assert loaded_config.number_of_commits == 5
    assert loaded_config.message_specifications == "concise and clear"
