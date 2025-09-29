"""Handles cli commands."""

from argparse import Namespace
from pathlib import Path

import pyperclip

from .ai_handler import suggest_commit_message
from .config import Config
from .git_handler import get_log, get_repository_changes


def handle_configure(args: Namespace) -> None:
    """Configure genie-git."""
    config = Config.load()

    if args.model:
        config.model = args.model
    if args.api_key:
        config.api_key = args.api_key
    if args.message_specifications:
        config.message_specifications = args.message_specifications

    # Check if both --always-copy and --always-copy-off are provided
    if args.always_copy and args.always_copy_off:
        raise ValueError("--always-copy and --always-copy-off cannot be used together.")
    if args.always_copy:
        config.always_copy = True
    if args.always_copy_off:
        config.always_copy = False
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
    config = Config.load()
    staged_changes = get_repository_changes(config.exclude_files)

    context = args.context or ""

    if not staged_changes:
        print("No staged changes found in the repository.")
        return

    git_logs = get_log(config.number_of_commits)

    message = suggest_commit_message(
        api_key=config.api_key,
        git_logs=git_logs,
        staged_changes=staged_changes,
        message_specifications=config.message_specifications,
        context=context,
    )
    if config.always_copy or args.copy:
        pyperclip.copy(message)
    print(message)
