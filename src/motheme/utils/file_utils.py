"""File-related utility functions."""

from pathlib import Path


def is_marimo_file(path: str) -> bool:
    """
    Check if a file is a Marimo notebook.

    A file is considered a Marimo notebook if it:
    1. Has .py extension
    2. Has an exact 'import marimo' line
    3. Creates a marimo.App instance
    4. Contains at least one @app.cell decorator

    Returns:
        bool: True if the file is a Marimo notebook, False otherwise.
        Non-text files or files with encoding issues are considered non-Marimo
            files.

    """
    if not str(path).endswith(".py"):
        return False

    try:
        with Path(path).open("r", encoding="utf-8", errors="strict") as file:
            lines = file.readlines()

            # Check for exact 'import marimo' line
            has_exact_import = "import marimo\n" in lines

            content = "".join(lines)
            has_app = "marimo.App(" in content
            has_cell = "@app.cell" in content

            return has_exact_import and has_app and has_cell
    except (UnicodeDecodeError, OSError):
        # If we can't read the file as UTF-8 or there are other IO issues,
        # it's definitely not a marimo file
        return False


def check_files_provided(
    action_description: str, files: tuple[str, ...]
) -> bool:
    """Check if files were provided and print error message if not."""
    if not files:
        print(
            f"Error: Please specify at least one file or directory "
            f"to {action_description}."
        )
        return False
    return True
