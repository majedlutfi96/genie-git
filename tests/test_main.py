"""Test the main module."""

from pytest_mock import MockerFixture

from genie_git.main import main


def test_main(mocker: MockerFixture) -> None:
    """Test that main sets up the parser correctly."""
    mock_create_parser = mocker.patch("genie_git.main.create_parser")

    mock_parser_instance = mocker.MagicMock()
    mock_create_parser.return_value = mock_parser_instance

    mock_parsed_args = mocker.MagicMock()
    mock_parser_instance.parse_args.return_value = mock_parsed_args

    main()

    mock_create_parser.assert_called_once()
    mock_parser_instance.parse_args.assert_called_once()
    mock_parsed_args.func.assert_called_once_with(mock_parsed_args)
