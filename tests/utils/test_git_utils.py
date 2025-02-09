"""Tests for git utility functions."""

import os
import subprocess
from pathlib import Path

import pytest

from motheme.utils.git_utils import expand_files, get_git_tracked_files

MARIMO_FILE_CONTENT = """import marimo
app = marimo.App()

@app.cell
def cell1():
    return 1
"""


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repo with some test files."""
    original_dir = Path.cwd()
    os.chdir(tmp_path)
    subprocess.run(["git", "init"], check=True)  # noqa: S603, S607

    # Create some test files
    (tmp_path / "test1.py").write_text(MARIMO_FILE_CONTENT)
    (tmp_path / "test2.py").write_text(MARIMO_FILE_CONTENT)
    (tmp_path / "not_marimo.py").write_text("print('hello')")

    # Create a subdirectory with files
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "test3.py").write_text(MARIMO_FILE_CONTENT)

    # Add files to git
    subprocess.run(["git", "add", "test1.py", "test2.py"], check=True)  # noqa: S603, S607
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)  # noqa: S603, S607

    yield tmp_path

    # Cleanup - return to original directory
    os.chdir(original_dir)


def test_get_git_tracked_files(git_repo) -> None:
    """Test getting git tracked files."""
    tracked_files = get_git_tracked_files()
    assert tracked_files == {"test1.py", "test2.py"}


def test_get_git_tracked_files_not_git_repo(tmp_path) -> None:
    """Test getting git tracked files in a non-git directory."""
    original_dir = Path.cwd()
    os.chdir(tmp_path)
    tracked_files = get_git_tracked_files()
    assert tracked_files == set()
    os.chdir(original_dir)


def test_expand_files_non_recursive(git_repo) -> None:
    """Test expanding files without recursion."""
    os.chdir(git_repo)  # Change to git repo directory for relative paths
    files = expand_files("test1.py", "test2.py", "not_marimo.py", recursive=False)
    assert sorted(files) == ["test1.py", "test2.py"]


def test_expand_files_recursive(git_repo) -> None:
    """Test expanding files with recursion."""
    os.chdir(git_repo)  # Change to git repo directory for relative paths
    files = expand_files(".", recursive=True)
    expected = [
        "subdir/test3.py",
        "test1.py",
        "test2.py",
    ]
    assert sorted(files) == sorted(expected)


def test_expand_files_with_git_ignore(git_repo) -> None:
    """Test expanding files with git ignore flag."""
    os.chdir(git_repo)  # Change to git repo directory for relative paths
    files = expand_files(".", recursive=True, git_ignore=True)
    expected = [
        "test1.py",
        "test2.py",
    ]
    assert sorted(files) == sorted(expected)


def test_expand_files_single_directory(git_repo) -> None:
    """Test expanding files for a single directory."""
    os.chdir(git_repo)  # Change to git repo directory for relative paths
    files = expand_files("subdir", recursive=True)
    expected = ["subdir/test3.py"]
    assert sorted(files) == sorted(expected)


def test_expand_files_non_existent() -> None:
    """Test expanding non-existent files."""
    files = expand_files("non_existent.py", recursive=False)
    assert files == []
