"""Module for downloading Marimo themes from a GitHub repository."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

import requests

from motheme.utils.theme_utils import get_themes_dir

if TYPE_CHECKING:
    from pathlib import Path


class HttpClient(Protocol):
    """Protocol for HTTP client."""

    def get(self, url: str, timeout: int = 10) -> requests.Response:
        """Make GET request."""
        ...


@dataclass
class ThemeDownloader:
    """Theme downloader with configurable dependencies."""

    http_client: HttpClient = requests
    themes_dir_getter: callable = get_themes_dir
    timeout: int = 10

    def _get_api_url(self, repo_url: str) -> str:
        """Convert GitHub repo URL to API URL."""
        return repo_url.replace(
            "https://github.com", "https://api.github.com/repos"
        )

    def _download_theme(
        self, api_base_url: str, theme_folder: dict, themes_dir: Path
    ) -> None:
        """Download a single theme CSS file."""
        theme_name = theme_folder["name"]
        css_file_url = (
            f"{api_base_url}/contents/themes/{theme_name}/{theme_name}.css"
        )

        css_response = self.http_client.get(css_file_url, timeout=self.timeout)
        css_response.raise_for_status()

        css_content = base64.b64decode(css_response.json()["content"]).decode(
            "utf-8"
        )

        css_path = themes_dir / f"{theme_name}.css"
        with css_path.open("w") as f:
            f.write(css_content)

        print(f"Downloaded: {css_path}")

    def download_themes(
        self,
        repo_url: str = "https://github.com/metaboulie/marimo-themes",
    ) -> Path | None:
        """
        Download Marimo themes CSS files from GitHub repository.

        Args:
            repo_url (str): GitHub repository URL

        Returns:
            Optional[Path]: Local directory where themes are stored,
                None if error occurs

        """
        themes_dir = self.themes_dir_getter()
        api_base_url = self._get_api_url(repo_url)
        themes_api_url = f"{api_base_url}/contents/themes"

        try:
            response = self.http_client.get(
                themes_api_url, timeout=self.timeout
            )
            response.raise_for_status()
            theme_folders = response.json()
            
            # Check for existing themes
            existing_themes = {
                theme.stem for theme in themes_dir.glob("*.css")
            }
            
            downloaded_count = 0
            skipped_count = 0

            for theme_folder in theme_folders:
                if theme_folder["type"] == "dir":
                    theme_name = theme_folder["name"]
                    if theme_name in existing_themes:
                        print(f"Theme '{theme_name}' is already downloaded")
                        skipped_count += 1
                    else:
                        self._download_theme(
                            api_base_url, theme_folder, themes_dir
                        )
                        downloaded_count += 1
            
            print(f"Downloaded {downloaded_count} themes, skipped {skipped_count} existing themes")

        except requests.RequestException as e:
            print(f"Error downloading themes: {e}")
            return None

        return themes_dir
        
    def download_specific_themes(
        self,
        theme_names: list[str],
        repo_url: str = "https://github.com/metaboulie/marimo-themes",
    ) -> tuple[list[str], list[str]]:
        """
        Download specific Marimo themes CSS files from GitHub repository.

        Args:
            theme_names: List of theme names to download
            repo_url (str): GitHub repository URL

        Returns:
            tuple[list[str], list[str]]: Tuple of (downloaded_themes, not_found_themes)
        """
        themes_dir = self.themes_dir_getter()
        api_base_url = self._get_api_url(repo_url)
        themes_api_url = f"{api_base_url}/contents/themes"
        
        downloaded_themes = []
        not_found_themes = []
        skipped_themes = []
        
        # Check for existing themes
        existing_themes = {
            theme.stem for theme in themes_dir.glob("*.css")
        }
        
        for theme_name in theme_names:
            if theme_name in existing_themes:
                print(f"Theme '{theme_name}' is already downloaded")
                skipped_themes.append(theme_name)
        
        # Only download themes that don't already exist
        themes_to_download = [
            name for name in theme_names 
            if name not in existing_themes
        ]
        
        if not themes_to_download:
            return downloaded_themes, not_found_themes
        
        try:
            response = self.http_client.get(
                themes_api_url, timeout=self.timeout
            )
            response.raise_for_status()
            theme_folders = response.json()
            
            available_themes = {
                folder["name"]: folder 
                for folder in theme_folders 
                if folder["type"] == "dir"
            }
            
            for theme_name in themes_to_download:
                if theme_name in available_themes:
                    try:
                        self._download_theme(
                            api_base_url, available_themes[theme_name], themes_dir
                        )
                        downloaded_themes.append(theme_name)
                    except requests.RequestException as e:
                        print(f"Error downloading theme {theme_name}: {e}")
                        not_found_themes.append(theme_name)
                else:
                    print(f"Theme '{theme_name}' not found in repository")
                    not_found_themes.append(theme_name)
                    
        except requests.RequestException as e:
            print(f"Error accessing themes repository: {e}")
            not_found_themes.extend(themes_to_download)
            
        return downloaded_themes, not_found_themes


# For backwards compatibility
def download_themes(
    repo_url: str = "https://github.com/metaboulie/marimo-themes",
) -> Path | None:
    """Backwards compatible function that uses default ThemeDownloader."""
    downloader = ThemeDownloader()
    return downloader.download_themes(repo_url)

def download_specific_themes(
    theme_names: list[str],
    repo_url: str = "https://github.com/metaboulie/marimo-themes",
) -> tuple[list[str], list[str]]:
    """
    Download specific Marimo themes from GitHub repository.
    
    Args:
        theme_names: List of theme names to download
        repo_url: GitHub repository URL
        
    Returns:
        tuple[list[str], list[str]]: Tuple of (downloaded_themes, not_found_themes)
    """
    downloader = ThemeDownloader()
    return downloader.download_specific_themes(theme_names, repo_url)
