"""Tests for theme utility functions."""


import appdirs
import pytest

from motheme.utils.theme_utils import get_themes_dir, validate_theme_exists


@pytest.fixture
def temp_themes_dir(tmp_path):
    """Create a temporary themes directory."""
    themes_dir = tmp_path / "themes"
    themes_dir.mkdir()
    return themes_dir


def test_validate_theme_exists_success(temp_themes_dir) -> None:
    """Test successful theme validation."""
    # Create a test theme file
    theme_name = "test_theme"
    theme_path = temp_themes_dir / f"{theme_name}.css"
    theme_path.write_text("/* Test CSS */")

    # Validate the theme exists
    result = validate_theme_exists(theme_name, temp_themes_dir)
    assert result == theme_path
    assert result.exists()


def test_validate_theme_exists_failure(temp_themes_dir, capsys) -> None:
    """Test theme validation when theme doesn't exist."""
    non_existent_theme = "non_existent_theme"

    # Create a test theme to show in available themes
    (temp_themes_dir / "existing_theme.css").write_text("/* Test CSS */")

    with pytest.raises(FileNotFoundError, match=f"Theme {non_existent_theme} not found"):
        validate_theme_exists(non_existent_theme, temp_themes_dir)

    # Check that proper error messages were printed
    captured = capsys.readouterr()
    assert "Error: Theme file" in captured.out
    assert "Available themes:" in captured.out
    assert "- existing_theme" in captured.out


def test_get_themes_dir(monkeypatch, tmp_path) -> None:
    """Test getting themes directory."""
    # Mock appdirs.user_data_dir to return our temp path
    test_data_dir = tmp_path / "test_data_dir"
    monkeypatch.setattr(appdirs, "user_data_dir", lambda *args: str(test_data_dir))

    # Get themes directory
    themes_dir = get_themes_dir()

    # Verify the directory exists and is correct
    assert themes_dir.exists()
    assert themes_dir == test_data_dir / "themes"
    assert themes_dir.is_dir()


def test_get_themes_dir_existing(monkeypatch, tmp_path) -> None:
    """Test getting themes directory when it already exists."""
    # Create the themes directory beforehand
    test_data_dir = tmp_path / "test_data_dir"
    themes_dir = test_data_dir / "themes"
    themes_dir.mkdir(parents=True)

    # Mock appdirs.user_data_dir
    monkeypatch.setattr(appdirs, "user_data_dir", lambda *args: str(test_data_dir))

    # Get themes directory
    result = get_themes_dir()

    # Verify the existing directory is used
    assert result == themes_dir
    assert result.exists()
    assert result.is_dir()
