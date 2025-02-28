# Marimo Custom Themes

> Personalize your experience with [marimo](https://github.com/marimo-team/marimo)

## Theme Gallery

<div align="center" style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;"> 
    
<table>
  <tr>
    <td>

<h3 style="text-align: center; margin-top: 0; color: #333;"><a href="themes/coldme/">coldme</a></h3> 

<div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;"> <img src="themes/coldme/coldme_light.png" alt="coldme light" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" /> <img src="themes/coldme/coldme_dark.png" alt="coldme dark" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" /> </div>

</td>
    <td>

<h3 style="text-align: center; margin-top: 0; color: #333;"><a href="themes/mininini/">mininini</a></h3> 
        
<div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;"> <img src="themes/mininini/mininini_light.png" alt="mininini light" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" /> <img src="themes/mininini/mininini_dark.png" alt="mininini dark" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" /> </div>

</td>
    <td>

<h3 style="text-align: center; margin-top: 0; color: #333;"><a href="themes/wigwam/">wigwam</a></h3> 
        
<div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;"> <img src="themes/wigwam/wigwam_light.png" alt="wigwam light" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" /> <img src="themes/wigwam/wigwam_dark.png" alt="wigwam dark" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" /> </div> </div>

</td>
  </tr>
</table>

</div>

## Get Started

<div align="center" style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;"> 
    
<table>
  <tr>
    <td>
        
<h3 style="text-align: center; margin-top: 0; color: #333;">With <a href="https://github.com/astral-sh/uv">uv</a> (recommended)</h3> 
        
```console
# Install motheme CLI tool
uvx motheme

# Help messages
uvx motheme -h

# Initialize themes
uvx motheme update

# List available themes
uvx motheme themes

# Apply a theme to specific files
uvx motheme apply coldme notebook1.py notebook2.py

# Or, apply theme recursively in a directory
uvx motheme apply -r coldme ./
```

</td>
    <td>

<h3 style="text-align: center; margin-top: 0; color: #333;">Or with pip</h3> 
        
```console
# Install motheme CLI tool
pip install motheme

# Help messages
motheme -h

# Initialize themes
motheme update

# List available themes
motheme themes

# Apply a theme to specific files
motheme apply coldme notebook1.py notebook2.py

# Or, apply theme recursively in a directory
motheme apply -r coldme ./
```

</td>
  </tr>
</table>

</div>

> [!NOTE]
>
> Please note that some parts of the Marimo notebook are not fully exposed for
> customization at this time, including side panels and cell editors

> [!WARNING]
>
> You may want to run `motheme clear -r ./` before sharing or uploading your notebooks
> because the field `css_file` in `marimo.App()` may leak your private data
