# Contributing to Motheme

Thank you for your interest in contributing to Motheme! This document will guide you
through the process of setting up your development environment and contributing to the
project.

## Development Setup

### Prerequisites

-   Python 3.9 or higher
-   [uv](https://github.com/astral-sh/uv) (recommended) or pip
-   [Hatch](https://hatch.pypa.io/) for development workflow

### Installation

1. Clone the repository:

```bash
git clone https://github.com/metaboulie/marimo-themes
cd marimo-themes
```

2. Install development dependencies:

```bash
uv pip install -e ".[dev,test]"
```

### Development Workflow

We use Hatch to manage our development workflow. Here are the common commands:

-   Format code:

```bash
hatch run format
```

-   Lint code:

```bash
hatch run lint
```

-   Run tests:

```bash
hatch run test:test
```

## Contributing Guidelines

### Adding Your Theme

1. **Study Default Theme**: All available arguments are listed in
   [`themes/default/default.css`](themes/default/default.css). Use this as a reference
   for writing your themes.

2. **Theme Requirements**:

    - Implement both light and dark themes using the light-dark syntax
    - If implementing only one mode, name it `xxx_light` or `xxx_dark` and use default
      values for the other mode
    - Test your theme with different notebook layouts and content types

3. **Folder Structure**:

    ```
    themes/
    └── your_theme_name/
        ├── <theme-name>.css
        ├── preview_light.png (optional)
        ├── preview_dark.png (optional)
        └── README.md (optional)
    ```

### Pull Request Process

1. Create a new branch for your changes
2. Follow the code style guidelines (enforced by Ruff)
3. Add tests for any new functionality
4. Update documentation as needed
5. Submit a pull request with a clear description of your changes

## Need Help?

If you have questions or need help, please:

1. Check existing issues and documentation
2. Open a new issue for bugs or feature requests
3. Start a discussion for general questions
