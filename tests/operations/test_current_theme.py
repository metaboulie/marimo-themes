"""Tests for current theme operations."""

from motheme.operations.current_theme import (
    extract_theme_name,
)


def test_extract_theme_name_with_theme() -> None:
    """Test extracting theme name from marimo.App line with theme."""
    line = 'marimo.App(css_file="themes/dark.css")'
    assert extract_theme_name(line) == "dark"

    # Test with single quotes
    line = "marimo.App(css_file='themes/light.css')"
    assert extract_theme_name(line) == "light"

    # Test with full marimo name
    line = 'marimo.App(css_file="themes/custom.css")'
    assert extract_theme_name(line) == "custom"


def test_extract_theme_name_without_theme() -> None:
    """Test extracting theme name from lines without theme."""
    # No css_file parameter
    line = "marimo.App()"
    assert extract_theme_name(line) is None

    # Not a marimo.App line
    line = "some other code"
    assert extract_theme_name(line) is None


