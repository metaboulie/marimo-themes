"""List available themes."""

from motheme.utils import get_themes_dir


def get_available_themes() -> list[str]:
    """
    Get list of available themes.

    Returns:
        list[str]: List of theme names without .css extension

    """
    themes_dir = get_themes_dir()
    if not themes_dir.exists():
        return []
    return sorted([theme.stem for theme in themes_dir.glob("*.css")])


def list_theme() -> None:
    """List available themes."""
    themes = get_available_themes()
    if themes:
        print("Available Themes:")
        for theme in themes:
            print(f"- {theme}")
    else:
        print("No themes downloaded. Run 'mtheme update' to download themes.")
