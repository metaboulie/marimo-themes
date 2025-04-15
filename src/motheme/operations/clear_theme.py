"""Clear theme from marimo notebooks."""

import re
from functools import lru_cache
from pathlib import Path

from motheme.utils import find_app_block, update_file_content


@lru_cache(maxsize=128)
def clean_app_line(line: str) -> str:
    """
    Remove css_file parameter and cleaning up punctuation.

    Args:
        line: The line containing marimo.App() call.

    Returns:
        Cleaned line with css_file parameter removed and punctuation fixed

    """
    # Remove css_file parameter and its value
    pattern = r',?\s*css_file=(["\'])(?:(?!\1).)*\1'
    new_line = re.sub(pattern, "", line)

    # Clean up any potential double commas or empty parentheses
    new_line = re.sub(r",\s*,", ",", new_line)
    new_line = re.sub(r"\(\s*,", "(", new_line)
    new_line = re.sub(r",\s*\)", ")", new_line)

    # Clean up any extra spaces between parentheses and parameters
    new_line = re.sub(r"\(\s+", "(", new_line)
    new_line = re.sub(r"\s+\)", ")", new_line)
    return re.sub(r"\s*,\s*", ", ", new_line)  # Normalize spaces around commas


def process_file(file_name: str) -> tuple[bool, list[str]]:
    """
    Process a single file to remove theme settings.

    Args:
        file_name: Path to the file to process

    Returns:
        Tuple of (success, modified_content)
        - success: True if theme was cleared, False if no theme found
        - modified_content: List of lines with theme removed

    """
    with Path(file_name).open("r") as f:
        content = f.readlines()

    app_block = find_app_block(content)
    if not app_block:
        return False, content

    if "css_file=" not in app_block.content:
        return False, content

    new_app_content = clean_app_line(app_block.content)
    new_content = update_file_content(content, app_block, new_app_content)

    return True, new_content


def clear_theme(files: list[str]) -> None:
    """
    Remove theme settings from specified notebook files.

    Args:
        files: List of Marimo notebook files to modify

    """
    modified_files = []
    current_file = None
    try:
        for file_name in files:
            current_file = file_name
            theme_cleared, new_content = process_file(file_name)

            if theme_cleared:
                with Path(file_name).open("w") as f:
                    f.writelines(new_content)
                modified_files.append(file_name)
                print(f"Cleared theme from {file_name}")
            else:
                print(f"No theme found in {file_name}")

    except OSError as e:
        print(f"Error processing {current_file}: {e}")

    # Summary
    if modified_files:
        print(f"\nSuccessfully cleared theme from {len(modified_files)} file(s).")
    else:
        print("No files were modified.")
