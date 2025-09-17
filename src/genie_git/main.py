"""Cli tool to suggest conventional git commit messages."""

from .cli import create_parser


def main() -> None:
    """Parse command-line arguments and execute the corresponding handler."""
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
