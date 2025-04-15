"""Font operations module."""

import re
from pathlib import Path
from shutil import copyfile

from motheme.utils import (
    get_fonts_dir,
    get_themes_dir,
    validate_font_exists,
    validate_theme_exists
)


def create_font(font_name: str, ref_font_name: str = "default") -> None:
    """
    Create a new font template by duplicating a reference font.

    Args:
        font_name: Name for the new font
        ref_font_name: Name of the reference font to duplicate, defaults to 'default'
    """
    fonts_dir = get_fonts_dir()
    
    # Check if the new font already exists
    new_font_path = fonts_dir / f"{font_name}.css"
    if new_font_path.exists():
        print(f"Error: Font '{font_name}' already exists.")
        return
    
    # Try to get reference font or create default if it doesn't exist
    ref_font_path = fonts_dir / f"{ref_font_name}.css"
    
    if not ref_font_path.exists():
        if ref_font_name == "default":
            # Create default font template
            with open(ref_font_path, "w") as f:
                f.write("""/* Font and Radius Variables */
:root {
    --monospace-font: var(--marimo-monospace-font, "Fira Mono", monospace);
    --text-font: var(--marimo-text-font, "PT Sans", sans-serif);
    --heading-font: var(--marimo-heading-font, "Lora", serif);
    --radius: 8px;
}
""")
            print(f"Created default font template: {ref_font_path}")
        else:
            print(f"Error: Reference font '{ref_font_name}' does not exist.")
            return
    
    # Copy the reference font to create new font
    copyfile(ref_font_path, new_font_path)
    print(f"Created new font template: {new_font_path}")


def set_font(font_name: str, *theme_names: str, all_themes: bool = False) -> None:
    """
    Apply a font template to one or more themes.

    Args:
        font_name: Name of the font template to apply
        theme_names: Names of themes to apply the font to
        all_themes: If True, apply to all installed themes
    """
    fonts_dir = get_fonts_dir()
    themes_dir = get_themes_dir()
    
    # Validate font exists
    try:
        font_path = validate_font_exists(font_name, fonts_dir)
    except FileNotFoundError:
        return
    
    # Read font template
    with open(font_path, "r") as f:
        font_content = f.read()
    
    # Get list of themes to update
    themes_to_update = []
    if all_themes:
        themes_to_update = [theme.stem for theme in themes_dir.glob("*.css")]
    else:
        if not theme_names:
            print("Error: Please specify at least one theme name or use --all.")
            return
        themes_to_update = list(theme_names)
    
    # Regular expression pattern to match the font section
    font_section_pattern = r":root\s*\{\s*--monospace-font:.*?\}"
    
    updated_themes = []
    failed_themes = []
    
    for theme_name in themes_to_update:
        try:
            theme_path = validate_theme_exists(theme_name, themes_dir)
            
            # Read theme content
            with open(theme_path, "r") as f:
                theme_content = f.read()
            
            # Check if theme has a font section
            if not re.search(font_section_pattern, theme_content, re.DOTALL):
                print(f"Warning: Theme '{theme_name}' doesn't have a font section to replace.")
                failed_themes.append(theme_name)
                continue
            
            # Replace font section
            updated_content = re.sub(font_section_pattern, font_content.strip(), theme_content, flags=re.DOTALL)
            
            # Write updated theme
            with open(theme_path, "w") as f:
                f.write(updated_content)
                
            updated_themes.append(theme_name)
            
        except FileNotFoundError:
            failed_themes.append(theme_name)
    
    if updated_themes:
        print(f"Successfully updated fonts for themes: {', '.join(updated_themes)}")
    if failed_themes:
        print(f"Failed to update fonts for themes: {', '.join(failed_themes)}")


def list_fonts() -> list[str]:
    """
    Get list of available font templates.

    Returns:
        list[str]: List of font template names without .css extension
    """
    fonts_dir = get_fonts_dir()
    if not fonts_dir.exists():
        return []
    
    return sorted([font.stem for font in fonts_dir.glob("*.css")]) 