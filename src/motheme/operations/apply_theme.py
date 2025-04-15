"""Apply a Marimo theme to specified notebook files."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from motheme.utils import (
    find_app_block,
    get_themes_dir,
    update_file_content,
    validate_theme_exists,
)


@lru_cache(maxsize=128)
def modify_app_line(line: str, css_file_path: Path) -> str:
    """Modify a marimo.App line to include or update the css_file parameter."""
    css_file_path = css_file_path.as_posix()
    if "css_file=" in line:
        # Replace existing css_file parameter
        return re.sub(
            r'css_file=["\'"][^"\']*["\']', f'css_file="{css_file_path}"', line
        )
    if line.strip().endswith("marimo.App()"):
        # No existing parameters
        return line.replace("marimo.App()", f'marimo.App(css_file="{css_file_path}")')
    # Has existing parameters, insert css_file
    return line.replace("marimo.App(", f'marimo.App(css_file="{css_file_path}", ')


def process_file(file_path: str, css_file_path: Path) -> tuple[bool, list[str]]:
    """Process a single file and return (success, new_content)."""
    with Path(file_path).open() as f:
        content = f.readlines()

    app_block = find_app_block(content)
    if not app_block:
        return False, content

    new_app_content = modify_app_line(app_block.content, css_file_path)
    new_content = update_file_content(content, app_block, new_app_content)

    return True, new_content


def apply_theme(
    theme_name: str, files: list[str]
) -> tuple[list[str], list[str], str | None]:
    """
    Apply a Marimo theme to specified notebook files.

    Args:
        theme_name: Name of the theme to apply
        files: List of Marimo notebook files to modify

    Returns:
        Tuple containing:
        - List of successfully modified files
        - List of files that failed to be modified
        - Error message if there was a critical error, None otherwise

    """
    # Validate theme
    themes_dir = get_themes_dir()
    try:
        css_file_path = validate_theme_exists(theme_name, themes_dir)
    except FileNotFoundError:
        return [], [], f"Theme '{theme_name}' not found in {themes_dir}"

    # Process files
    modified_files = []
    failed_files = []
    current_file = None
    try:
        for file_name in files:
            current_file = file_name
            theme_applied, new_content = process_file(file_name, css_file_path)

            if theme_applied:
                try:
                    with Path(file_name).open("w") as f:
                        f.writelines(new_content)
                        print(f"Applied theme {theme_name} to {file_name}")
                    modified_files.append(file_name)
                except OSError:
                    failed_files.append(file_name)
                    print(f"Failed to apply theme {theme_name} to {file_name}")
            else:
                failed_files.append(file_name)
                print(f"Failed to apply theme {theme_name} to {file_name}")

    except OSError as e:
        return (
            modified_files,
            failed_files,
            f"Error processing {current_file}: {e}",
        )

    print(f"Applied theme {theme_name} to {len(modified_files)} files")
    print(f"Failed to apply theme {theme_name} to {len(failed_files)} files")

    return modified_files, failed_files, None
