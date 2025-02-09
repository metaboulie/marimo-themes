import pytest
from pathlib import Path
from motheme.apply_theme import modify_app_line


@pytest.fixture
def sample_css_path():
    return Path("C:/themes/new.css")


def test_modify_app_line_add_css_no_params(sample_css_path):
    line = "app = marimo.App()"
    expected = 'app = marimo.App(css_file="C:/themes/new.css")'
    assert modify_app_line(line, sample_css_path) == expected


def test_modify_app_line_replace_existing_css(sample_css_path):
    line = 'app = marimo.App(css_file="C:/themes/old.css", width=800)'
    expected = 'app = marimo.App(css_file="C:/themes/new.css", width=800)'
    assert modify_app_line(line, sample_css_path) == expected


def test_modify_app_line_insert_css_with_existing_params(sample_css_path):
    line = "app = marimo.App(width=800, height=600)"
    expected = 'app = marimo.App(css_file="C:/themes/new.css", width=800, height=600)'
    assert modify_app_line(line, sample_css_path) == expected
