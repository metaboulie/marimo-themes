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


def get_fonts_dir() -> Path:
    """Get the fonts directory path."""
    fonts_dir = Path(appdirs.user_data_dir("motheme", "marimo")) / "fonts"
    if not fonts_dir.exists():
        fonts_dir.mkdir(parents=True, exist_ok=True)
    return fonts_dir


def validate_font_exists(font_name: str, fonts_dir: Path) -> Path:
    """Validate font exists and return its path."""
    css_file_path = fonts_dir / f"{font_name}.css"
    if not css_file_path.exists():
        print(f"Error: Font file {css_file_path} does not exist.")
        print("Available fonts:")
        for font in fonts_dir.glob("*.css"):
            print(f"- {font.stem}")
        msg = f"Font {font_name} not found"
        raise FileNotFoundError(msg)
    return css_file_path
