# Avalanche Warning Attributes Update

## Summary

Updated the Varsom integration to use **avalanche-specific attributes** instead of generic warning text fields for avalanche warnings, providing more relevant and detailed information.

## What Changed

### Before (Generic Attributes)
Avalanche warnings used the same generic attributes as landslide and flood warnings:
- `warning_text` - Not available in avalanche API
- `advice_text` - Not available in avalanche API  
- `consequence_text` - Not available in avalanche API

### After (Avalanche-Specific Attributes)
Avalanche warnings now include rich, avalanche-specific information:

| Attribute | Description | Type | Example |
|-----------|-------------|------|---------|
| `main_text` | Primary warning message | string | "Persistent weak layer near the surface..." |
| `avalanche_danger` | Detailed danger description | string | "Den kraftige vinden vil fortsatt føre til..." |
| `emergency_warning` | Emergency warning text | string | Emergency warnings when applicable |
| `avalanche_problems` | Specific problem types | list | Problem type details and triggers |
| `avalanche_advices` | Safety advice with images | list | Structured advice with visual aids |
| `snow_surface` | Current snow conditions | string | "Det har kommet et par centimeter nysnø..." |
| `current_weaklayers` | Weak layers in snowpack | string | "Det finnes et svakt lag av kantkorn..." |
| `latest_avalanche_activity` | Recent avalanche observations | string | Recent avalanche reports |
| `latest_observations` | Latest field observations | string | "Onsdag er det meldt om skytende spreker..." |
| `mountain_weather` | Mountain weather impact | dict | Weather conditions affecting stability |
| `forecaster` | Warning author/forecaster | string | "Snøskredvarslingen 26128" |
| `danger_level_name` | Human-readable danger level | string | "3 Considerable" |
| `exposed_height` | Elevation where danger applies | int | Elevation data |

### Geographical Attributes (Existing)
These remain unchanged for avalanche warnings:
- `region_id` - Avalanche region ID
- `region_name` - Avalanche region name
- `utm_zone` - UTM coordinate zone
- `utm_east` - UTM east coordinate
- `utm_north` - UTM north coordinate

### Generic Attributes (Landslide/Flood Only)
Non-avalanche warnings still use:
- `warning_text` - Warning description
- `advice_text` - Safety advice
- `consequence_text` - Potential consequences

## Technical Implementation

### API Changes
- **AvalancheAPI** (`api.py`): Now extracts all avalanche-specific fields from NVE API
- **Sensor** (`sensor.py`): Conditionally uses avalanche attributes vs generic attributes based on warning type

### Code Locations
- `custom_components/varsom/api.py` (lines ~198-218): Added avalanche-specific field extraction
- `custom_components/varsom/sensor.py` (lines ~384-415): Conditional attribute assignment

## Benefits

1. **More Relevant Information**: Users get avalanche-specific details instead of generic warning text
2. **Richer Data**: Structured information about problems, advice, snow conditions, and observations
3. **Better UX**: Avalanche experts can now access technical details like weak layers and recent activity
4. **Future-Proof**: Uses the full range of data available from NVE's avalanche API

## Validation

✅ Generic warning/advice/consequence fields removed from avalanche warnings  
✅ Avalanche-specific fields successfully extracted from API  
✅ Backwards compatibility maintained for landslide/flood warnings  
✅ All avalanche-specific data now available in Home Assistant attributes