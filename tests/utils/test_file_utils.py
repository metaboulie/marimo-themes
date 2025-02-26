"""Tests for file utility functions."""

import os
import tempfile

from motheme.utils.file_utils import check_files_provided, is_marimo_file


def test_is_marimo_file_valid() -> None:
    """Test that a valid Marimo notebook is correctly identified."""
    valid_content = """import marimo
app = marimo.App()

@app.cell
def _(mo):
    print("Hello World")
    return mo
"""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(valid_content)
        temp_path = f.name

    try:
        assert is_marimo_file(temp_path) is True
    finally:
        os.unlink(temp_path)


def test_is_marimo_file_non_python() -> None:
    """Test that non-Python files are rejected."""
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
        f.write("import marimo\n@app.cell\nmarimo.App()")
        temp_path = f.name

    try:
        assert is_marimo_file(temp_path) is False
    finally:
        os.unlink(temp_path)


def test_is_marimo_file_missing_elements() -> None:
    """Test that Python files missing required Marimo elements are rejected."""
    test_cases = [
        # Missing import
        """
app = marimo.App()
@app.cell
def _(mo): pass
""",
        # Missing App instance
        """import marimo
@app.cell
def _(mo): pass
""",
        # Missing cell decorator
        """import marimo
app = marimo.App()
def _(mo): pass
""",
    ]

    for content in test_cases:
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            assert is_marimo_file(temp_path) is False
        finally:
            os.unlink(temp_path)


def test_is_marimo_file_nonexistent() -> None:
    """Test behavior with nonexistent file."""
    assert is_marimo_file("/nonexistent/path/file.py") is False


def test_check_files_provided_empty(capsys) -> None:
    """Test check_files_provided with empty tuple."""
    assert check_files_provided("test", ()) is False
    captured = capsys.readouterr()
    assert "Error: Please specify at least one file or directory" in captured.out


def test_check_files_provided_with_files() -> None:
    """Test check_files_provided with non-empty tuple."""
    assert check_files_provided("test", ("file1.py", "file2.py")) is True
