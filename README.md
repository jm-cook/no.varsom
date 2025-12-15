# Varsom Alerts - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom integration that provides landslide and flood warnings from NVE (Norwegian Water Resources and Energy Directorate) via the Varsom.no API.

## Features

- **Single sensor per county** - Clean, modern design with all alerts in attributes
- **Landslide and flood warnings** - Choose one or both warning types
- **County-based alerts** - Select your Norwegian county
- **Activity levels** - Green (1), Yellow (2), Orange (3), Red (4)
- **Rich alert data** - Includes warning text, advice, consequences, municipalities, and more
- **Direct links** - Each alert includes a link to Varsom.no with an interactive map
- **Bilingual** - Support for Norwegian and English
- **Official Yr.no icons** - Uses the same warning icons as Yr.no and Varsom.no

## Installation

### Manual Installation

1. Copy the `custom_components/varsom` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Varsom Alerts"

### HACS Installation

1. Add this repository as a custom repository in HACS
2. Search for "Varsom Alerts" in HACS
3. Install the integration
4. Restart Home Assistant
5. Go to Settings → Devices & Services → Add Integration

## Configuration

The integration is configured through the UI:

1. Select your **County** (e.g., Vestland, Rogaland, etc.)
2. Choose **Warning Type**:
   - Landslide only
   - Flood only
   - Both
3. Select **Language** (Norwegian or English)

## Sensor Data

The integration creates a single sensor per configuration with the following structure:

### State

The sensor state is the **highest activity level** (1-4) from all active warnings:
- `1` = Green (no warnings)
- `2` = Yellow (moderate danger)
- `3` = Orange (considerable danger)
- `4` = Red (high/extreme danger)

### Attributes

```yaml
active_alerts: 2
highest_level: "yellow"
highest_level_numeric: 2
county_name: "Vestland"
county_id: "46"
alerts:
  - id: "584731"
    level: 2
    level_name: "yellow"
    danger_type: "Jord- og flomskredfare"
    warning_type: "landslide"
    municipalities:
      - "Tysnes"
      - "Bergen"
      - "Stord"
    valid_from: "2025-12-14T07:00:00"
    valid_to: "2025-12-15T06:59:00"
    danger_increases: "2025-12-14T16:00:00"
    danger_decreases: "2025-12-15T19:00:00"
    main_text: "Moderate avalanche danger..."
    warning_text: "Up to 150mm precipitation expected..."
    advice_text: "Stay informed about weather..."
    consequence_text: "Landslides may occur..."
    url: "https://www.varsom.no/en/flood-and-landslide-warning-service/forecastid/584731"
```

## Usage Examples

### Automation - Alert Notification

```yaml
automation:
  - alias: "Varsom Yellow Alert Notification"
    trigger:
      - platform: numeric_state
        entity_id: sensor.varsom_landslide_vestland
        above: 1
    action:
      - service: notify.mobile_app
        data:
          title: "Landslide Warning"
          message: >
            {{ state_attr('sensor.varsom_landslide_vestland', 'alerts')[0].main_text }}
          data:
            url: "{{ state_attr('sensor.varsom_landslide_vestland', 'alerts')[0].url }}"
```

### Template Sensor - Municipality Filter

```yaml
template:
  - sensor:
      - name: "Bergen Landslide Alert"
        state: >
          {% set alerts = state_attr('sensor.varsom_landslide_vestland', 'alerts') | 
                          selectattr('municipalities', 'search', 'Bergen') | list %}
          {{ alerts[0].level_name if alerts else 'green' }}
        attributes:
          alert_count: >
            {% set alerts = state_attr('sensor.varsom_landslide_vestland', 'alerts') | 
                            selectattr('municipalities', 'search', 'Bergen') | list %}
            {{ alerts | length }}
```

### Lovelace Card

```yaml
type: entities
title: Landslide Warnings
entities:
  - entity: sensor.varsom_landslide_vestland
    name: Vestland Alert Level
    icon: mdi:mountain
    type: custom:template-entity-row
    state: >
      {{ states('sensor.varsom_landslide_vestland') }} - 
      {{ state_attr('sensor.varsom_landslide_vestland', 'highest_level') | upper }}
  - type: attribute
    entity: sensor.varsom_landslide_vestland
    attribute: active_alerts
    name: Active Alerts
```

## API Information

This integration uses the official NVE API:

- **Landslide API**: `https://api01.nve.no/hydrology/forecast/landslide/v1.0.10/api`
- **Flood API**: `https://api01.nve.no/hydrology/forecast/flood/v1.0.10/api`
- **Update Interval**: 30 minutes
- **Documentation**: https://api.nve.no/doc/

### Language Support

The language option you select during setup controls both:
- ✅ The alert text language (Norwegian or English from the API via Språknøkkel parameter)
- ✅ The language of the Varsom.no website links (Norwegian or English interface)

The API uses the Språknøkkel path parameter:
- `1` = Norwegian (LangKey: 1 in response)
- `2` = English (LangKey: 2 in response)

## Supported Counties

- Oslo (03)
- Rogaland (11)
- Møre og Romsdal (15)
- Nordland (18)
- Viken (30)
- Innlandet (34)
- Vestfold og Telemark (38)
- Agder (42)
- Vestland (46)
- Trøndelag (50)
- Troms og Finnmark (54)

## Development

Based on the Met Alerts integration pattern with improvements:

- ✅ Single sensor with attribute array (not multiple sensors)
- ✅ Modern coordinator pattern
- ✅ Config flow with validation
- ✅ Rich alert data in attributes
- ✅ Direct links to Varsom.no maps

## Credits

- **Author**: Jeremy Cook (@jm-cook)
- **Data Source**: NVE (Norwegian Water Resources and Energy Directorate)
- **Website**: https://www.varsom.no/
- **Warning Icons**: Yr warning icons © 2015 by Yr/NRK, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## License

This integration is provided as-is under the MIT License.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Note**: This integration is not affiliated with NVE or Varsom.no. It simply provides an interface to their public API for use in Home Assistant.
