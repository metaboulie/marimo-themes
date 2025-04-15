"""Remove theme files."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from motheme.utils import get_themes_dir

if TYPE_CHECKING:
    from pathlib import Path


def get_theme_status(
    theme_names: list[str], themes_dir: Path | None = None
) -> tuple[list[str], list[str]]:
    """
    Check which themes exist and which don't.

    Args:
        theme_names: List of theme names to check
        themes_dir: Optional directory path, uses default if not provided

    Returns:
        Tuple of (existing_themes, non_existing_themes)

    """
    if themes_dir is None:
        themes_dir = get_themes_dir()

    existing_themes = []
    non_existing_themes = []

    for theme in theme_names:
        theme_path = themes_dir / f"{theme}.css"
        if theme_path.exists():
            existing_themes.append(theme)
        else:
            non_existing_themes.append(theme)

    return existing_themes, non_existing_themes


def remove_theme_files(
    theme_names: list[str],
    themes_dir: Path | None = None,
    confirm_func: Callable[[str], bool] | None = None,
    print_func: Callable[[str], None] | None = None,
) -> tuple[list[str], list[str]]:
    """
    Remove theme files from themes directory.

    Args:
        theme_names: List of theme names to remove
        themes_dir: Optional directory path, uses default if not provided
        confirm_func: Optional function to handle confirmation,
            defaults to interactive prompt
        print_func: Optional function to handle output, defaults to print

    Returns:
        Tuple of (removed_themes, non_existing_themes)

    """
    if themes_dir is None:
        themes_dir = get_themes_dir()
    if print_func is None:
        print_func = print
    if confirm_func is None:

        def confirm_func(msg: str) -> bool:
            return input(msg).lower().strip() == "y"

    existing_themes, non_existing_themes = get_theme_status(theme_names, themes_dir)

    if non_existing_themes:
        print_func("Following themes do not exist:")
        for theme in non_existing_themes:
            print_func(f"- {theme}")

    if not existing_themes:
        return [], non_existing_themes

    print_func(f"Will remove themes: {', '.join(existing_themes)}")
    if not confirm_func("Continue? (y/n): "):
        print_func("Operation cancelled")
        return [], non_existing_themes

    removed_themes = []
    for theme in existing_themes:
        theme_path = themes_dir / f"{theme}.css"
        theme_path.unlink()
        removed_themes.append(theme)
        print_func(f"Removed theme: {theme}")

    return removed_themes, non_existing_themes
