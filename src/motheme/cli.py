"""CLI for motheme."""

import arguably

from motheme.operations import (
    apply_theme,
    clear_theme,
    create_theme,
    current_theme,
    list_theme,
    remove_theme_files,
)
from motheme.utils import (
    check_files_provided,
    download_specific_themes,
    download_themes,
    expand_files,
    quiet_mode,
)


@arguably.command
def update() -> None:
    """Update Marimo themes from GitHub repository."""
    print("\033[93mWARNING: The 'update' command is deprecated and will be removed in v0.4.0. "
          "Use 'motheme download --all' instead.\033[0m")
    download_themes()


@arguably.command
def themes() -> None:
    """List available Marimo themes."""
    list_theme()


@arguably.command
def download(
    *theme_names: str,
    all_themes: bool = False,
) -> None:
    """
    Download specific Marimo themes.

    Args:
        theme_names: Names of themes to download
        all_themes: [-a/--all] If True, download all available themes
    """
    if all_themes:
        print("Downloading all available themes...")
        download_themes()
        return

    if not theme_names:
        print("Error: Please specify at least one theme name to download or use --all.")
        print("       Run 'mtheme themes' to see available themes.")
        return

    print(f"Downloading themes: {', '.join(theme_names)}")
    downloaded, not_found = download_specific_themes(list(theme_names))

    if downloaded:
        print(f"Successfully downloaded: {', '.join(downloaded)}")
    if not_found:
        print(f"Themes not found or failed to download: {', '.join(not_found)}")
        print("Run 'mtheme themes' to see available themes.")


@arguably.command
def apply(
    theme_name: str,
    *files: str,
    recursive: bool = False,
    quiet: bool = False,
    git_ignore: bool = False,
) -> None:
    """
    Apply a Marimo theme to specified notebook files.

    Args:
        theme_name: Name of the theme to apply
        files: Tuple of file/directory paths
        recursive: [-r] If True, recursively search directories for
            Marimo notebooks
        quiet: [-q] If True, suppress output
        git_ignore: [-i] If True, ignore files that are not tracked by git

    """
    if not check_files_provided("apply the theme", files):
        return

    with quiet_mode(enabled=quiet):
        apply_theme(
            theme_name,
            expand_files(*files, recursive=recursive, git_ignore=git_ignore),
        )


@arguably.command
def clear(
    *files: str,
    recursive: bool = False,
    quiet: bool = False,
    git_ignore: bool = False,
) -> None:
    """
    Remove theme settings from specified notebook files.

    Args:
        files: Tuple of file/directory paths
        recursive: [-r] If True, recursively search directories for
            Marimo notebooks
        quiet: [-q] If True, suppress output
        git_ignore: [-i] If True, ignore files that are not tracked by git

    """
    if not check_files_provided("clear themes from", files):
        return

    with quiet_mode(enabled=quiet):
        clear_theme(
            expand_files(*files, recursive=recursive, git_ignore=git_ignore)
        )


@arguably.command
def current(
    *files: str,
    recursive: bool = False,
    quiet: bool = False,
    git_ignore: bool = False,
) -> None:
    """
    Show currently applied themes for specified notebook files.

    Args:
        files: Tuple of file/directory paths
        recursive: [-r] If True, recursively search directories for
            Marimo notebooks
        quiet: [-q] If True, suppress output
        git_ignore: [-i] If True, ignore files that are not tracked by git

    """
    if not check_files_provided("check themes for", files):
        return

    with quiet_mode(enabled=quiet):
        current_theme(
            expand_files(*files, recursive=recursive, git_ignore=git_ignore)
        )


@arguably.command
def remove(*theme_names: str, all_themes: bool = False) -> None:
    """
    Remove specified theme files from themes directory.

    Args:
        theme_names: Names of themes to remove
        all_themes: [-a/--all] If True, remove all installed themes

    """
    from motheme.operations.list_theme import get_available_themes

    if all_themes:
        remove_theme_files(get_available_themes())
        return

    if not theme_names:
        print("Error: Please specify at least one theme name to remove.")
        return

    remove_theme_files(list(theme_names))


@arguably.command
def create(ref_theme_name: str, theme_name: str) -> None:
    """
    Create a new theme by duplicating an existing theme.

    Args:
        ref_theme_name: Name of the reference theme to duplicate
        theme_name: Name for the new theme

    """
    create_theme(ref_theme_name, theme_name)


def main() -> None:
    """CLI entry point."""
    arguably.run()


if __name__ == "__main__":
    main()
