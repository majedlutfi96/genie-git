"""Cli tool to suggest conventional git commit messages."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from .config import Config


def handle_configure(args: Namespace) -> None:
    """Configure git-genie."""
    config = Config.load()

    if args.model:
        config.model = args.model
    if args.api_key:
        config.api_key = args.api_key
    if args.message_specifications:
        config.message_specifications = args.message_specifications

    if args.show:
        config.show()

    config.save()


def handle_exclude_files(args: Namespace) -> None:
    """Exclude files from the diff."""
    files = args.files
    # Verify if the files exist
    for file in files:
        if not Path(file).exists():
            raise FileNotFoundError(f"File {file} does not exist.")

    config = Config.load()
    config.exclude_files.extend(files)
    config.save()


def handle_suggest(args: Namespace) -> None:
    """Suggests a commit message based on the changes in the repository."""
    raise NotImplementedError("handle_suggest is not implemented yet.")


def main() -> None:
    """Parse command-line arguments and execute the corresponding function."""
    parser = ArgumentParser(
        "git-genie",
        description="An AI-powered tool to suggest conventional git commit messages.",
    )

    parser.set_defaults(func=handle_suggest)

    subparsers = parser.add_subparsers(dest="command")

    parser_suggest = subparsers.add_parser(
        "suggest",
        help="Suggests a commit message based on the changes in the repository.",
    )
    parser_suggest.set_defaults(func=handle_suggest)

    parser_configure = subparsers.add_parser(
        "configure", help="Configures Google API Key and other settings."
    )
    parser_configure.add_argument(
        "--model",
        help=(
            "The model to use for generating the commit message"
            "[Default: gemini-2.5-flash]."
        ),
    )
    parser_configure.add_argument(
        "--api-key",
        help=(
            "The API key to use for generating the commit message."
            "[You can generate a free google genai API key by visiting:"
            "https://aistudio.google.com/apikey]"
        ),
    )
    parser_configure.add_argument(
        "--message-specifications",
        help="Additional specifications for the commit message.",
    )
    parser_configure.add_argument(
        "--number-of-commits",
        help="The number of commits to include in the AI prompt as a reference.",
    )
    parser_configure.add_argument(
        "--show",
        action="store_true",
        help="Show the current config.",
    )
    parser_configure.set_defaults(func=handle_configure)

    parser_exclude_files = subparsers.add_parser(
        "exclude-files", help="Add files to exclude from the diff."
    )
    parser_exclude_files.add_argument(
        "files", nargs="+", help="The files to exclude from the diff."
    )
    parser_exclude_files.set_defaults(func=handle_exclude_files)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
