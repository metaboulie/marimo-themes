"""Theme-related utility functions."""

from pathlib import Path

import appdirs


def validate_theme_exists(theme_name: str, themes_dir: Path) -> Path:
    """Validate theme exists and return its path."""
    css_file_path = themes_dir / f"{theme_name}.css"
    if not css_file_path.exists():
        print(f"Error: Theme file {css_file_path} does not exist.")
        print("Available themes:")
        for theme in themes_dir.glob("*.css"):
            print(f"- {theme.stem}")
        msg = f"Theme {theme_name} not found"
        raise FileNotFoundError(msg)
    return css_file_path


def get_themes_dir() -> Path:
    """Get the themes directory path."""
    themes_dir = Path(appdirs.user_data_dir("motheme", "marimo")) / "themes"
    if not themes_dir.exists():
        themes_dir.mkdir(parents=True, exist_ok=True)
    return themes_dir
