"""Show current theme of marimo notebooks."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from motheme.utils import find_app_block


@lru_cache(maxsize=128)
def extract_theme_name(line: str) -> str | None:
    """
    Extract theme name from marimo.App line.

    Args:
        line: The line containing marimo.App() call

    Returns:
        Theme name if found, None otherwise

    """
    if "marimo.App(" not in line:
        return None

    match = re.search(r'css_file=["\'](.*?)["\']', line)
    if not match:
        return None

    # Extract theme name from path
    css_path = Path(match.group(1))
    return css_path.stem


def read_file_content(file_path: str | Path) -> list[str]:
    """
    Read file content safely.

    Args:
        file_path: Path to the file to read

    Returns:
        List of lines in the file

    Raises:
        OSError: If file cannot be read

    """
    with Path(file_path).open("r") as f:
        return f.readlines()


def current_theme(files: list[str]) -> dict[str, str | None]:
    """
    Get currently applied themes for specified notebook files.

    Args:
        files: List of Marimo notebook files to check

    Returns:
        Dictionary mapping file names to their theme names
        (or None if no theme)

    """
    results = {}

    for file_name in files:
        try:
            content = read_file_content(file_name)
            app_block = find_app_block(content)

            if not app_block:
                results[file_name] = None
                continue

            theme_name = extract_theme_name(app_block.content)
            if theme_name:
                print(f"{file_name}: {theme_name}")
            else:
                print(f"{file_name}: No theme applied")

        except OSError as e:
            print(f"Error processing {file_name}: {e!s}")
    return results
