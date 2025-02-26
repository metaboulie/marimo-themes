"""Git-related utility functions."""

import subprocess
from pathlib import Path


class GitPathError(Exception):
    """Raised when a path is not in the git repository's directory."""


def get_git_tracked_files() -> set[str]:
    """
    Get list of files tracked by git in the current directory.

    Returns:
        Set of tracked file paths relative to current directory.
        Empty set if not in a git repository or on error.

    """
    try:
        output = subprocess.check_output(  # noqa: S603
            ["git", "ls-files"],  # noqa: S607
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return {path.strip() for path in output.splitlines()}
    except (
        subprocess.SubprocessError,
        subprocess.CalledProcessError,
        OSError,
    ):
        print("Error: Not in a git repository")
        return set()


def expand_files(
    *files: str, recursive: bool, git_ignore: bool = False
) -> list[str]:
    """
    Expand file paths, optionally recursively for directories.
    Only includes valid Marimo notebook files.

    Args:
        files: Tuple of file/directory paths
        recursive: If True, recursively search directories for Python files
        git_ignore: If True, skip files that are git ignored

    Returns:
        List of expanded file paths that are Marimo notebooks

    """
    if git_ignore:
        tracked_files = get_git_tracked_files()

    def is_tracked(path: str) -> bool:
        try:
            return (
                not git_ignore
                or str(Path(path).resolve().relative_to(Path.cwd()))
                in tracked_files
            )
        except ValueError as e:
            msg = (
                f"The file '{path}' is not in the current directory. "
                "Please run the command from the directory containing "
                "your notebooks or use the '-i' flag in the correct directory."
            )
            raise GitPathError(msg) from e

    if not recursive:
        from .file_utils import is_marimo_file

        return [f for f in files if is_marimo_file(f) and is_tracked(f)]

    expanded_files = []
    for file in files:
        path = Path(file)
        if path.is_dir():
            # Find all .py files and filter for Marimo notebooks
            from .file_utils import is_marimo_file

            expanded_files.extend(
                str(f)
                for f in path.rglob("*.py")
                if is_marimo_file(str(f)) and is_tracked(str(f))
            )
        elif is_marimo_file(str(path)) and is_tracked(str(path)):
            expanded_files.append(str(path))
    return expanded_files
