# [Marimo](https://github.com/marimo-team/marimo) Custom Themes

> [!NOTE]
>
> Some parts of the Marimo notebook are not fully exposed for customization at this
> time

> [!WARNING]
>
> You may want to run `motheme clear -r ./` before sharing or uploading your notebooks
> because the field `css_file` in `marimo.App()` may leak your private data

## Theme Gallery

<div align="center">

**Ayu**

<img src="themes/ayu/ayu_light.png" alt="Ayu Light" width="45%" />
<img src="themes/ayu/ayu_dark.png" alt="Ayu Dark" width="45%" />

**Gruvbox**

<img src="themes/gruvbox/gruvbox_light.png" alt="Gruvbox Light" width="45%" />
<img src="themes/gruvbox/gruvbox_dark.png" alt="Gruvbox Dark" width="45%" />

**Solarized**

<img src="themes/solarized/solarized_light.png" alt="Solarized Light" width="45%" />
<img src="themes/solarized/solarized_dark.png" alt="Solarized Dark" width="45%" />

</div>

## Installation

### Using pip

```console
# Install motheme CLI tool
pip install motheme
```

### Using uv

```console
# Install motheme CLI tool
uvx motheme
```

### Using git (development)

```console
# Clone the repository
git clone https://github.com/metaboulie/marimo-themes.git
cd marimo-themes

# Install the package in development mode
pip install -e .
```

## Usage

### Synopsis

```
motheme [-h | --help] [--version]
        <command> [<args>]

These are common motheme commands:

Theme management
   ls          List available themes and fonts
   download    Download themes from repository
   apply       Apply a theme to notebook files
   clear       Remove theme settings from notebooks
   current     Show current theme for notebooks
   create      Create a new theme by copying an existing one
   remove      Remove theme files from themes directory

Font template management
   font        Manage font templates for themes
```

### Commands

#### motheme ls

```
motheme ls [--all | -a] [--all-themes] [--installed] [--not-installed] [--custom] [--font]

    --all, -a           List all available themes and fonts with attributes
    --all-themes        List all available themes
    --installed         List installed themes (default if no flag specified)
    --not-installed     List themes that are not installed
    --custom            List custom themes
    --font              List all font templates
```

#### motheme download

```
motheme download [<theme_name>...] [--all | -a]

    <theme_name>...     Names of themes to download
    --all, -a           Download all available themes
```

#### motheme apply

```
motheme apply <theme_name> <file>... [--recursive | -r] [--quiet | -q] [--git-ignore | -i]

    <theme_name>        Name of the theme to apply
    <file>...           File/directory paths
    --recursive, -r     Recursively search directories for Marimo notebooks
    --quiet, -q         Suppress output
    --git-ignore, -i    Ignore files that are not tracked by git
```

#### motheme clear

```
motheme clear <file>... [--recursive | -r] [--quiet | -q] [--git-ignore | -i]

    <file>...           File/directory paths
    --recursive, -r     Recursively search directories for Marimo notebooks
    --quiet, -q         Suppress output
    --git-ignore, -i    Ignore files that are not tracked by git
```

#### motheme current

```
motheme current <file>... [--recursive | -r] [--quiet | -q] [--git-ignore | -i]

    <file>...           File/directory paths
    --recursive, -r     Recursively search directories for Marimo notebooks
    --quiet, -q         Suppress output
    --git-ignore, -i    Ignore files that are not tracked by git
```

#### motheme create

```
motheme create <ref_theme_name> <theme_name>

    <ref_theme_name>    Name of the reference theme to duplicate
    <theme_name>        Name for the new theme
```

#### motheme remove

```
motheme remove [<theme_name>...] [--all | -a]

    <theme_name>...     Names of themes to remove
    --all, -a           Remove all installed themes
```

#### motheme font

```
motheme font <subcommand> [<args>]

Subcommands:
    ls          List available font templates
    set         Apply a font template to themes
    create      Create a new font template
    validate    Validate font template structure
```

##### motheme font ls

```
motheme font ls

    Lists all available font templates
```

##### motheme font set

```
motheme font set <font_name> [<theme_name>...] [--all | -a]

    <font_name>         Name of the font template to apply
    <theme_name>...     Names of themes to apply the font to
    --all, -a           Apply to all installed themes
```

##### motheme font create

```
motheme font create <font_name> [<ref_font_name>]

    <font_name>         Name for the new font
    <ref_font_name>     Name of the reference font to duplicate (defaults to 'default')
```

##### motheme font validate

```
motheme font validate <font_name>

    <font_name>         Name of the font template to validate
```

### Workflow Examples

#### Complete Theme Setup

```console
# 1. Check available themes
motheme ls --not-installed

# 2. Download desired themes
motheme download ayu nord

# 3. Apply theme to your notebooks
motheme apply ayu my_notebook.py

# 4. Check which theme is applied
motheme current my_notebook.py
```

#### Customizing Fonts

```console
# 1. List available font templates
motheme font ls

# 2. Create a custom font template
motheme font create my_custom_font

# 3. Apply the font to themes
motheme font set my_custom_font ayu nord

# 4. Apply the themed font to notebooks
motheme apply ayu my_notebook.py
```

#### Creating Custom Themes

```console
# 1. Create a new theme based on an existing one
motheme create ayu my_custom_theme

# 2. Apply your custom theme
motheme apply my_custom_theme my_notebook.py
```
