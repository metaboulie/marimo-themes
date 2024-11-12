"""Show current theme of marimo notebooks."""

from __future__ import annotations

import re
from pathlib import Path

from .app_parser import find_app_block


def extract_theme_name(line: str) -> str | None:
    """
    Extract theme name from marimo.App line.

    Args:
        line: The line containing marimo.App() call

    Returns:
        Theme name if found, None otherwise

    """
    # Look for css_file parameter
    match = re.search(r'css_file=["\'](.*?)["\']', line)
    if not match:
        return None

    # Extract theme name from path
    css_path = Path(match.group(1))
    return css_path.stem


def current_theme(files: list[str]) -> None:
    """
    Show currently applied themes for specified notebook files.

    Args:
        files: List of Marimo notebook files to check

    """
    found_themes = False
    try:
        for file_name in files:
            with Path(file_name).open("r") as f:
                content = f.readlines()

            app_block = find_app_block(content)
            if not app_block:
                print(f"No marimo.App found in {file_name}")
                continue

            theme_name = extract_theme_name(app_block.content)
            if theme_name:
                found_themes = True
                print(f"{file_name}: {theme_name}")
            else:
                print(f"{file_name}: No theme applied")

    except OSError as e:
        print(f"Error processing {file_name}: {e}")

    if not found_themes:
        print("\nNo themes found in any files.")
