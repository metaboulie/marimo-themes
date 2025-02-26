"""Tests for theme downloader module."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
import requests

from motheme.utils.theme_downloader import ThemeDownloader


class MockResponse:
    """Mock HTTP response."""

    def __init__(self, status_code: int, content: dict | str) -> None:
        self.status_code = status_code
        self._content = content

    def json(self):
        """Return JSON content."""
        return self._content

    def raise_for_status(self) -> None:
        """Raise exception if status code >= 400."""
        if self.status_code >= 400:
            msg = f"HTTP {self.status_code}"
            raise requests.HTTPError(msg)


@pytest.fixture
def mock_http_client():
    """Create a mock HTTP client."""
    return Mock()


@pytest.fixture
def mock_themes_dir(tmp_path):
    """Create a temporary themes directory."""
    themes_dir = tmp_path / "themes"
    themes_dir.mkdir()
    return lambda: themes_dir


@pytest.fixture
def theme_downloader(mock_http_client, mock_themes_dir):
    """Create a ThemeDownloader instance with mocked dependencies."""
    return ThemeDownloader(
        http_client=mock_http_client,
        themes_dir_getter=mock_themes_dir,
    )


def test_get_api_url() -> None:
    """Test GitHub URL to API URL conversion."""
    downloader = ThemeDownloader()
    github_url = "https://github.com/user/repo"
    expected = "https://api.github.com/repos/user/repo"
    assert downloader._get_api_url(github_url) == expected


def test_successful_theme_download(theme_downloader, mock_http_client, mock_themes_dir) -> None:
    """Test successful theme download."""
    # Mock API responses
    themes_list = [
        {
            "name": "test-theme",
            "type": "dir",
        }
    ]
    theme_content = {
        "content": "LyogVGVzdCBDU1MgKi8=",  # Base64 encoded "/* Test CSS */"
    }

    def mock_get(url: str, timeout: int):
        if url.endswith("/contents/themes"):
            return MockResponse(200, themes_list)
        if url.endswith(".css"):
            return MockResponse(200, theme_content)
        msg = f"Unexpected URL: {url}"
        raise ValueError(msg)

    mock_http_client.get.side_effect = mock_get

    # Execute download
    result = theme_downloader.download_themes("https://github.com/user/repo")

    # Verify results
    assert result == mock_themes_dir()
    theme_file = result / "test-theme.css"
    assert theme_file.exists()
    assert theme_file.read_text() == "/* Test CSS */"


def test_download_with_network_error(theme_downloader, mock_http_client) -> None:
    """Test theme download with network error."""
    mock_http_client.get.side_effect = requests.RequestException("Network error")

    result = theme_downloader.download_themes()
    assert result is None


def test_download_with_invalid_response(theme_downloader, mock_http_client) -> None:
    """Test theme download with invalid API response."""
    mock_http_client.get.return_value = MockResponse(404, {})

    result = theme_downloader.download_themes()
    assert result is None


def test_download_with_empty_themes(theme_downloader, mock_http_client, mock_themes_dir) -> None:
    """Test theme download with no themes available."""
    mock_http_client.get.return_value = MockResponse(200, [])

    result = theme_downloader.download_themes()
    assert result == mock_themes_dir()
    # Verify no files were created
    assert len(list(mock_themes_dir().glob("*.css"))) == 0


def test_download_with_non_dir_items(theme_downloader, mock_http_client, mock_themes_dir) -> None:
    """Test theme download with non-directory items in response."""
    themes_list = [
        {"name": "not-a-theme", "type": "file"},
        {"name": "test-theme", "type": "dir"},
    ]
    theme_content = {
        "content": "LyogVGVzdCBDU1MgKi8=",
    }

    def mock_get(url: str, timeout: int):
        if url.endswith("/contents/themes"):
            return MockResponse(200, themes_list)
        if url.endswith(".css"):
            return MockResponse(200, theme_content)
        msg = f"Unexpected URL: {url}"
        raise ValueError(msg)

    mock_http_client.get.side_effect = mock_get

    result = theme_downloader.download_themes()
    assert result == mock_themes_dir()
    # Verify only the theme directory was processed
    theme_files = list(mock_themes_dir().glob("*.css"))
    assert len(theme_files) == 1
    assert theme_files[0].name == "test-theme.css"
