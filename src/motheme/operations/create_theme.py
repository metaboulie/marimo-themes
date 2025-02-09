"""Create a new theme by duplicating an existing theme."""

from shutil import copyfile

from motheme.utils import get_themes_dir, validate_theme_exists


def create_theme(ref_theme_name: str, theme_name: str) -> None:
    """
    Create a new theme by duplicating an existing theme.

    Args:
        ref_theme_name: Name of the reference theme to duplicate
        theme_name: Name for the new theme

    """
    themes_dir = get_themes_dir()

    # Validate reference theme exists
    ref_theme_path = validate_theme_exists(ref_theme_name, themes_dir)

    # Create new theme path
    new_theme_path = themes_dir / f"{theme_name}.css"

    # Check if new theme already exists
    if new_theme_path.exists():
        print(f"Error: Theme '{theme_name}' already exists.")
        return

    # Copy the reference theme to create new theme
    copyfile(ref_theme_path, new_theme_path)
    print(f"Created new theme: {new_theme_path}")
