"""Apply a Marimo theme to specified notebook files."""

import re
from functools import lru_cache
from pathlib import Path

from .app_parser import find_app_block, update_file_content
from .util import get_themes_dir, validate_theme_exists


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
        return line.replace(
            "marimo.App()", f'marimo.App(css_file="{css_file_path}")'
        )
    # Has existing parameters, insert css_file
    return line.replace(
        "marimo.App(", f'marimo.App(css_file="{css_file_path}", '
    )


def process_file(
    file_path: str, css_file_path: Path
) -> tuple[bool, list[str]]:
    """Process a single file and return (success, new_content)."""
    with Path(file_path).open() as f:
        content = f.readlines()

    app_block = find_app_block(content)
    if not app_block:
        return False, content

    new_app_content = modify_app_line(app_block.content, css_file_path)
    new_content = update_file_content(content, app_block, new_app_content)

    return True, new_content


def apply_theme(theme_name: str, files: list[str]) -> None:
    """
    Apply a Marimo theme to specified notebook files.

    :param theme_name: Name of the theme to apply
    :param files: List of Marimo notebook files to modify
    """
    # Validate theme
    themes_dir = get_themes_dir()
    try:
        css_file_path = validate_theme_exists(theme_name, themes_dir)
    except FileNotFoundError:
        return

    # Process files
    modified_files = []
    current_file = None
    try:
        for file_name in files:
            current_file = file_name
            theme_applied, new_content = process_file(file_name, css_file_path)

            if theme_applied:
                with Path(file_name).open("w") as f:
                    f.writelines(new_content)
                modified_files.append(file_name)
                print(f"Applied {theme_name} theme to {file_name}")
            else:
                print(f"Failed to apply {theme_name} theme to {file_name}")

    except OSError as e:
        print(f"Error processing {current_file}: {e}")

    # Summary
    if modified_files:
        print(
            f"\nSuccessfully applied {theme_name} theme to "
            f"{len(modified_files)} file(s)."
        )
    else:
        print("No files were modified.")
