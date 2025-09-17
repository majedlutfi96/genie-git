"""Test the CLI module."""

from genie_git.cli import create_parser
from genie_git.cli_handlers import (
    handle_configure,
    handle_exclude_files,
    handle_suggest,
)


def parser_defaults_to_suggest() -> None:
    """Test that the parser defaults to suggest."""
    parser = create_parser()
    args = parser.parse_args([])
    assert args.func == handle_suggest


def parser_calls_configure_handler() -> None:
    """Test that the parser calls the configure handler correctly."""
    parser = create_parser()
    args = parser.parse_args(
        [
            "configure",
            "--model",
            "test_model",
            "--api-key",
            "test_api_key",
            "--message-specifications",
            "test_message_specifications",
        ]
    )
    assert args.func == handle_configure
    assert args.model == "test_model"
    assert args.api_key == "test_api_key"
    assert args.message_specifications == "test_message_specifications"
    assert args.show is False


def parser_calls_exclude_files_handler() -> None:
    """Test that the parser calls the exclude files handler correctly."""
    parser = create_parser()
    args = parser.parse_args(["exclude-files", "test_file1", "test_file2"])
    assert args.func == handle_exclude_files
    assert args.files == ["test_file1", "test_file2"]
