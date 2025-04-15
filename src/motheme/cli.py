"""CLI for motheme."""

import arguably
import requests

from motheme.operations import (
    apply_theme,
    clear_theme,
    create_font,
    create_theme,
    current_theme,
    list_fonts,
    list_theme,
    remove_theme_files,
    set_font,
)
from motheme.utils import (
    check_files_provided,
    download_specific_themes,
    download_themes,
    expand_files,
    get_themes_dir,
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
    print("\033[93mWARNING: The 'themes' command is deprecated and will be removed in v0.4.0. "
          "Use 'motheme ls' instead.\033[0m")
    list_theme()


@arguably.command
def ls(
    *,
    list_all: bool = False,
    all_themes: bool = False,
    installed: bool = False,
    not_installed: bool = False,
    custom: bool = False,
    font: bool = False,
) -> None:
    """
    List themes and fonts with various filtering options.
    
    Args:
        list_all: [-a/--all] List all available themes and fonts with attributes
        all_themes: [--all-themes] List all available themes
        installed: [--installed] List installed themes
        not_installed: [--not-installed] List themes that are not installed
        custom: [--custom] List custom themes
        font: [--font] List all font templates
    """
    # If no flags are provided, show installed themes by default
    if not any([list_all, all_themes, installed, not_installed, custom, font]):
        installed = True
    
    themes_dir = get_themes_dir()
    
    # Get all installed themes
    local_themes = [theme.stem for theme in themes_dir.glob("*.css")]
    
    # Get remote available themes
    remote_themes = []
    if not_installed or list_all or all_themes or custom:
        try:
            repo_url = "https://github.com/metaboulie/marimo-themes"
            api_url = repo_url.replace("https://github.com", "https://api.github.com/repos")
            themes_api_url = f"{api_url}/contents/themes"
            
            response = requests.get(themes_api_url, timeout=10)
            response.raise_for_status()
            theme_folders = response.json()
            
            remote_themes = [
                folder["name"] for folder in theme_folders 
                if folder["type"] == "dir"
            ]
        except requests.RequestException as e:
            print(f"Warning: Could not fetch remote themes: {e}")

    # Get fonts
    fonts = []
    if font or list_all:
        fonts = list_fonts()
    
    # Determine which themes are custom (not in remote repo)
    custom_themes = [theme for theme in local_themes if theme not in remote_themes]
    
    # Handle --installed flag
    if installed and not (list_all or all_themes):
        if local_themes:
            print("Installed Themes:")
            for theme in sorted(local_themes):
                print(f"- {theme}")
        else:
            print("No themes installed. Run 'motheme download' to download themes.")
    
    # Handle --not-installed flag
    if not_installed and not (list_all or all_themes):
        not_installed_themes = [theme for theme in remote_themes if theme not in local_themes]
        if not_installed_themes:
            print("Available Themes (Not Installed):")
            for theme in sorted(not_installed_themes):
                print(f"- {theme}")
        else:
            print("All available themes are already installed.")
    
    # Handle --custom flag
    if custom and not (list_all or all_themes):
        if custom_themes:
            print("Custom Themes:")
            for theme in sorted(custom_themes):
                print(f"- {theme}")
        else:
            print("No custom themes found.")
    
    # Handle --font flag
    if font and not (list_all or all_themes):
        if fonts:
            print("Font Templates:")
            for font_name in sorted(fonts):
                print(f"- {font_name}")
        else:
            print("No font templates found.")
    
    # Handle --all or -a flag
    if list_all or all_themes:
        # Get not installed themes
        not_installed_themes = [theme for theme in remote_themes if theme not in local_themes]
        
        # Standard installed themes (not custom)
        standard_themes = [theme for theme in local_themes if theme in remote_themes]
        
        # Find max length for alignment
        all_names = standard_themes + custom_themes + not_installed_themes
        if list_all:
            all_names.extend(fonts)
        max_length = max([len(name) for name in all_names]) if all_names else 0
        
        title = "All Themes and Fonts:" if list_all else "All Themes:"
        print(title)
        
        # Print installed standard themes
        for theme in sorted(standard_themes):
            print(f"- {theme:{max_length}} \033[92m[installed]\033[0m")
        
        # Print custom themes
        for theme in sorted(custom_themes):
            print(f"- {theme:{max_length}} \033[94m[custom]\033[0m")
        
        # Print not installed themes
        for theme in sorted(not_installed_themes):
            print(f"- {theme:{max_length}} \033[93m[not installed]\033[0m")
        
        # Print fonts only for list_all
        if list_all:
            for font_name in sorted(fonts):
                print(f"- {font_name:{max_length}} \033[95m[font]\033[0m")
        
        if not (standard_themes or custom_themes or not_installed_themes or (list_all and fonts)):
            print("No themes" + (" or fonts" if list_all else "") + " found.")


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


@arguably.command
def font() -> None:
    """Font operations for Marimo themes."""


@arguably.command
def font__set(
    font_name: str,
    *theme_names: str,
    all_themes: bool = False,
) -> None:
    """
    Apply a font template to specified theme(s).

    Args:
        font_name: Name of the font template to apply
        theme_names: Names of themes to apply the font to
        all_themes: [-a/--all] If True, apply to all installed themes
    """
    set_font(font_name, *theme_names, all_themes=all_themes)


@arguably.command
def font__create(
    font_name: str,
    ref_font_name: str = "default",
) -> None:
    """
    Create a new font template by duplicating a reference font.

    Args:
        font_name: Name for the new font
        ref_font_name: Name of the reference font to duplicate (defaults to 'default')
    """
    create_font(font_name, ref_font_name)


@arguably.command
def font__list() -> None:
    """List available font templates."""
    fonts = list_fonts()
    if not fonts:
        print("No font templates found.")
        return
    
    print("Available font templates:")
    for font in fonts:
        print(f"- {font}")


def main() -> None:
    """CLI entry point."""
    arguably.run()


if __name__ == "__main__":
    main()
