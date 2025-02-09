"""Tests for apply_theme operations."""

import os
import tempfile
from pathlib import Path

from motheme.operations.apply_theme import (
    modify_app_line,
    process_file,
)


def test_modify_app_line_no_existing_params() -> None:
    """Test modifying app line with no existing parameters."""
    line = "marimo.App()"
    css_path = Path("themes/dark.css")
    result = modify_app_line(line, css_path)
    assert result == 'marimo.App(css_file="themes/dark.css")'


def test_modify_app_line_with_existing_params() -> None:
    """Test modifying app line with existing parameters."""
    line = 'marimo.App(title="My App")'
    css_path = Path("themes/dark.css")
    result = modify_app_line(line, css_path)
    assert result == 'marimo.App(css_file="themes/dark.css", title="My App")'


def test_modify_app_line_replace_existing_css() -> None:
    """Test replacing existing css_file parameter."""
    line = 'marimo.App(css_file="old.css")'
    css_path = Path("themes/dark.css")
    result = modify_app_line(line, css_path)
    assert result == 'marimo.App(css_file="themes/dark.css")'


def test_process_file() -> None:
    """Test processing a file with app block."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("""import marimo

app = marimo.App()
marimo.md("# Hello")
""")
        temp_path = f.name

    try:
        success, content = process_file(temp_path, Path("themes/dark.css"))
        assert success
        assert any('marimo.App(css_file="themes/dark.css")' in line for line in content)
    finally:
        os.unlink(temp_path)


def test_process_file_no_app_block() -> None:
    """Test processing a file without app block."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("""import marimo

marimo.md("# Hello")
""")
        temp_path = f.name

    try:
        success, content = process_file(temp_path, Path("themes/dark.css"))
        assert not success
        assert content == ["import marimo\n", "\n", 'marimo.md("# Hello")\n']
    finally:
        os.unlink(temp_path)
