"""Parser for marimo.App declarations in notebook files."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AppBlock:
    """
    Represents a marimo.App block in a notebook file.

    An example of an App block is:

    ```python
    app = marimo.App(
        css_file="path/to/theme.css",
    )
    ```
    """

    start_line: int
    """The line number of the first line of the App block."""
    end_line: int
    """The line number of the last line of the App block."""
    content: str
    """The content of the App block."""


def find_app_block(content: list[str]) -> AppBlock | None:
    """
    Find and extract the marimo.App block from file content.

    Returns None if no App block is found.
    """
    in_app_block = False
    app_block_lines = []
    open_parentheses = 0
    start_line = -1

    for i, line in enumerate(content):
        if "app = marimo.App(" in line:
            in_app_block = True
            start_line = i
            open_parentheses = line.count("(") - line.count(")")
            app_block_lines = [line]

            if open_parentheses == 0:
                # Single line case
                return AppBlock(
                    start_line=i,
                    end_line=i,
                    content="".join(app_block_lines),
                )
            continue

        if in_app_block:
            open_parentheses += line.count("(") - line.count(")")
            app_block_lines.append(line.strip())

            if open_parentheses == 0:
                return AppBlock(
                    start_line=start_line,
                    end_line=i,
                    content="".join(app_block_lines),
                )

    return None


def update_file_content(
    file_content: list[str], app_block: AppBlock, new_content: str
) -> list[str]:
    """Replace the App block in the file content with new content."""
    return (
        [*file_content[:app_block.start_line], new_content, *file_content[app_block.end_line + 1:]]
    )
