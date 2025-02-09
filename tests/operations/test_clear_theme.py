"""Tests for clear_theme operations."""

import os
import tempfile

from motheme.operations.clear_theme import (
    clean_app_line,
    process_file,
)


def test_clean_app_line_basic() -> None:
    """Test removing css_file parameter with no other parameters."""
    line = 'marimo.App(css_file="themes/dark.css")'
    result = clean_app_line(line)
    assert result == "marimo.App()"


def test_clean_app_line_with_other_params() -> None:
    """Test removing css_file parameter while preserving other parameters."""
    line = 'marimo.App(css_file="themes/dark.css", title="My App")'
    result = clean_app_line(line)
    assert result == 'marimo.App(title="My App")'


def test_clean_app_line_css_file_middle() -> None:
    """Test removing css_file parameter from middle of parameter list."""
    line = 'marimo.App(title="My App", css_file="themes/dark.css", width=800)'
    result = clean_app_line(line)
    assert result == 'marimo.App(title="My App", width=800)'


def test_clean_app_line_no_css_file() -> None:
    """Test line with no css_file parameter remains unchanged."""
    line = 'marimo.App(title="My App")'
    result = clean_app_line(line)
    assert result == line


def test_process_file() -> None:
    """Test processing a file with app block containing css_file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("""import marimo

app = marimo.App(css_file="themes/dark.css")
marimo.md("# Hello")
""")
        temp_path = f.name

    try:
        success, content = process_file(temp_path)
        assert success
        assert "marimo.App()" in "".join(content)
        assert "css_file" not in "".join(content)
    finally:
        os.unlink(temp_path)


def test_process_file_with_other_params() -> None:
    """Test processing a file with app block containing css_file and other parameters."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("""import marimo

app = marimo.App(title="My App", css_file="themes/dark.css", width=800)
marimo.md("# Hello")
""")
        temp_path = f.name

    try:
        success, content = process_file(temp_path)
        assert success
        assert 'marimo.App(title="My App", width=800)' in "".join(content)
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
        success, content = process_file(temp_path)
        assert not success
        assert content == ["import marimo\n", "\n", 'marimo.md("# Hello")\n']
    finally:
        os.unlink(temp_path)


def test_process_file_no_css_file() -> None:
    """Test processing a file with app block but no css_file parameter."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("""import marimo

app = marimo.App(title="My App")
marimo.md("# Hello")
""")
        temp_path = f.name

    try:
        success, content = process_file(temp_path)
        assert not success
        assert content == ["import marimo\n", "\n", 'app = marimo.App(title="My App")\n', 'marimo.md("# Hello")\n']
    finally:
        os.unlink(temp_path)
