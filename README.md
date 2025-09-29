# genie-git

[![codecov](https://codecov.io/gh/majedlutfi96/genie-git/branch/develop/graph/badge.svg?token=SU461946FV)](https://codecov.io/gh/majedlutfi96/genie-git)

An AI-powered CLI tool to suggest conventional commit messages for your staged files.

## Why genie-git?

Writing well-formatted, conventional commit messages is a best practice, but it can be tedious. `genie-git` uses the power of Google's Gemini models to analyze your staged changes and instantly propose a high-quality commit message for you.

## Features

-   **AI-Powered Suggestions**: Automatically generates commit messages based on your staged changes.
-   **Conventional Commits**: Enforces a consistent and readable commit history.
-   **Customizable**: Configure the AI model, API key, and message specifications to fit your needs.
-   **Exclude Files**: Easily exclude files from the diff to fine-tune your commit message.
-   **Clipboard Integration**: Copy commit messages directly to your clipboard for easy pasting.
-   **Context-Aware**: Provide additional context to improve AI suggestions.

## Installation

Install `genie-git` directly from PyPI:

```bash
pip install genie-git
```

## Quick Start

1.  **Get your Google API Key:**

    You can generate a free Google Generative AI API key by visiting [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

2.  **Configure `genie-git`:**

    Set up your API key with the following command:

    ```bash
    genie-git configure --api-key YOUR_API_KEY
    ```

That's it! You're now ready to generate commit messages.

## Usage

### Suggest a Commit Message

To get a commit message suggestion, simply run `genie-git` in your repository:

```bash
genie-git suggest
```

This will analyze your staged changes and output a suggested commit message.

#### Additional Options for Suggest Command

You can enhance your commit message suggestions with these options:

```bash
# Provide additional context to the AI
genie-git suggest --context "This fixes the login bug reported by users"

# Copy the commit message directly to clipboard
genie-git suggest --copy

# Combine context and clipboard copying
genie-git suggest --context "Refactoring for better performance" --copy
```

**Available suggest options:**

-   `--context`: Provide additional context to help the AI generate better commit messages.
-   `--copy`: Copy the generated commit message to the clipboard.

### Advanced Configuration

While only an API key is needed to get started, you can further customize `genie-git` to fit your workflow:

```bash
genie-git configure --model gemini-1.5-pro --message-specifications "My custom instructions"
```

#### Clipboard Configuration

You can configure automatic clipboard copying:

```bash
# Enable automatic clipboard copying for all commit messages
genie-git configure --always-copy

# Disable automatic clipboard copying
genie-git configure --always-copy-off

# Show current configuration
genie-git configure --show
```

**Available configuration options:**

-   `--api-key`: Your Google Generative AI API key.
-   `--model`: The model to use (e.g., `gemini-1.5-flash`).
-   `--message-specifications`: Additional instructions for the AI.
-   `--number-of-commits`: The number of recent commits to use as a reference.
-   `--always-copy`: Enable automatic clipboard copying for all commit messages.
-   `--always-copy-off`: Disable automatic clipboard copying.
-   `--show`: Display the current configuration.

### Exclude Files

To exclude files from the diff, use the `exclude-files` command:

```bash
genie-git exclude-files file1.txt path/to/file2.py
```
