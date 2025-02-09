# Marimo Custom Themes

> personalize your experience with [marimo](https://github.com/marimo-team/marimo)

## Theme Gallery

### <a href="themes/coldme/">coldme</a>

<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    <img src="themes/coldme/coldme_light.png" alt="coldme light" width="400" "/>
    <img src="themes/coldme/coldme_dark.png" alt="coldme dark" width="400"/>
</div>

### <a href="themes/nord/">nord</a>

<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    <img src="themes/nord/nord_light.png" alt="nord light" width="400" "/>
    <img src="themes/nord/nord_dark.png" alt="nord dark" width="400"/>
</div>

### <a href="themes/mininini/">mininini</a>

<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    <img src="themes/mininini/mininini_light.png" alt="mininini light" width="400" "/>
    <img src="themes/mininini/mininini_dark.png" alt="mininini dark" width="400"/>
</div>

### <a href="themes/wigwam/">wigwam</a>

<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    <img src="themes/wigwam/wigwam_light.png" alt="wigwam light" width="400" "/>
    <img src="themes/wigwam/wigwam_dark.png" alt="wigwam dark" width="400"/>
</div>

## Get Started

```bash
# Install motheme CLI tool
pip install motheme

# Help messages
motheme

# Initialize themes
motheme update

# List available themes
motheme themes

# Apply a theme to specific files
motheme apply coldme notebook1.py notebook2.py

# Or, apply theme recursively in a directory
motheme apply -r coldme ./
```

> [!NOTE]
>
> Please note that some parts of the Marimo notebook are not fully exposed for
> customization at this time. This includes side panels and cell editors

> [!WARNING]
>
> You may want to run `motheme clear -r ./` before sharing or uploading your notebooks
> because the field `css_file` in `marimo.App()` may leak your private data

You can also run `motheme` as a uv tool

```bash
# use motheme
uvx motheme <command>
```

## Alternative

If you are using marimo in a browser like Firefox, you can use tools like
[Dark Reader](https://addons.mozilla.org/en-US/firefox/addon/darkreader/) for theming
with or without motheme

## Usage

-   **Requirements**: Ensure you are using Marimo version **0.9.14** or higher. It is
    recommended to keep your Marimo version up-to-date for the best experience

-   **Light and Dark Mode Support**: All themes support both light and dark modes and
    will switch automatically based on your notebook's current theme settings
