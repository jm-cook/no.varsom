# Yr.no Warning Icons

This integration uses the official Yr.no warning icons for visual consistency with Norway's weather services.

## Automatic (No Setup Required)

The SVG icons are **embedded directly in the integration** using base64 encoding. No manual file copying or setup is required!

The integration will automatically display the appropriate warning icon based on:
- Warning type (landslide or flood)
- Alert level (yellow, orange, or red)

## Icons Included

The following icons are embedded in the integration:

- **Landslide warnings**:
  - Yellow (level 2) - Landslide danger
  - Orange (level 3) - Severe landslide danger  
  - Red (level 4) - Extreme landslide danger

- **Flood warnings**:
  - Yellow (level 2) - Flood danger
  - Orange (level 3) - Severe flood danger
  - Red (level 4) - Extreme flood danger

## Icon Source

Icons are from the official Yr.no warning icon set:
- **Repository**: https://github.com/nrkno/yr-warning-icons
- **Website**: https://nrkno.github.io/yr-warning-icons/
- **License**: CC BY 4.0 (Creative Commons Attribution 4.0 International)
- **Copyright**: Yr warning icons © 2015 by Yr/NRK
- **Format**: SVG embedded as base64 data URLs

### License Details

The icons are free to use under the CC BY 4.0 license, which requires:
- ✅ Attribution to Yr/NRK (provided in this integration)
- ✅ Link to the license (https://creativecommons.org/licenses/by/4.0/)
- ✅ Indication if changes were made (icons are used unmodified, only base64 encoded)

Full license text: https://creativecommons.org/licenses/by/4.0/legalcode

## How It Works

The icons are stored as base64-encoded SVG data URLs in `const.py`. Home Assistant displays them via the `entity_picture` property, which means:
- ✅ No external files needed
- ✅ Works immediately after installation
- ✅ No www folder setup required
- ✅ Icons work in all themes

## Using Custom Icons

If you prefer Material Design Icons or custom icons instead, you can override them in Home Assistant:

1. Go to **Settings** → **Devices & Services**
2. Click on the entity
3. Click the gear icon (settings)
4. Set a custom icon (e.g., `mdi:alert-circle`) or entity picture URL

## Technical Details

For developers: The SVG files in `custom_components/varsom/icons/` are converted to base64 and stored in `ICON_DATA_URLS` dict in `const.py`. The sensor's `entity_picture` property returns the appropriate data URL based on warning type and level.
