# Complete Dashboard Setup for Tysnes/Bergen Area

## How It Works

When you set a municipality filter (e.g., "Tysnes, Bergen"), the integration automatically creates **two sensors**:

1. **`sensor.varsom_landslide_vestland`** - All alerts for the entire county
2. **`sensor.varsom_landslide_my_area`** - Only alerts affecting your filtered municipalities

No template sensors needed!

## Step 1: Configure the Integration

1. Go to Settings → Devices & Services → Varsom Alerts → Configure
2. Set Municipality Filter: `Tysnes, Bergen`
3. Save and reload the integration

You'll now have two sensors automatically:
- `sensor.varsom_landslide_vestland` (all county alerts)
- `sensor.varsom_landslide_my_area` (only your area)

## Step 2: Simple Dashboard Card

### Minimal Card (Recommended)

```yaml
type: vertical-stack
cards:
  # Status overview
  - type: entities
    title: Landslide Warnings
    entities:
      - entity: sensor.varsom_landslide_my_area
        name: My Area (Tysnes/Bergen)
        secondary_info: last-changed
      - type: attribute
        entity: sensor.varsom_landslide_my_area
        attribute: active_alerts
        name: Active Alerts
  
  # Show details when active
  - type: conditional
    conditions:
      - entity: sensor.varsom_landslide_my_area
        state_not: "1"
    card:
      type: markdown
      title: ⚠️ Active Warnings
      content: |
        {% set alerts = state_attr('sensor.varsom_landslide_my_area', 'alerts') %}
        {% for alert in alerts %}
        ### {{ alert.level_name|upper }} Alert
        
        **Municipalities**: {{ alert.municipalities|join(', ') }}
        
        {{ alert.main_text }}
        
        **Valid until**: {{ alert.valid_to[:16] }}
        
        [📍 View Map on Varsom.no]({{ alert.url }})
        
        ---
        {% endfor %}
```

### Compact Single Card

```yaml
type: markdown
title: My Area Warnings
content: |
  {% set alerts = state_attr('sensor.varsom_landslide_my_area', 'alerts') %}
  {% if alerts and alerts|length > 0 %}
    {% for alert in alerts %}
  **{{ alert.level_name|upper }}**: {{ alert.municipalities|join(', ') }}
  {{ alert.main_text[:100] }}... [Details]({{ alert.url }})
  ---
    {% endfor %}
  {% else %}
  ✅ No warnings for your area
  {% endif %}
```

### Glance Card (Status Overview)

```yaml
type: glance
title: Warning Status
entities:
  - entity: sensor.varsom_landslide_my_area
    name: My Area
  - entity: sensor.varsom_landslide_vestland
    name: All County
columns: 2
```

## Step 3: Mobile Notifications

```yaml
automation:
  - alias: "Landslide Warning - My Area"
    trigger:
      - platform: numeric_state
        entity_id: sensor.varsom_landslide_my_area
        above: 1
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "⚠️ Landslide Warning"
          message: |
            Level: {{ state_attr('sensor.varsom_landslide_my_area', 'highest_level')|upper }}
            
            {% set alerts = state_attr('sensor.varsom_landslide_my_area', 'alerts') %}
            {{ alerts[0].main_text }}
          data:
            url: |
              {% set alerts = state_attr('sensor.varsom_landslide_my_area', 'alerts') %}
              {{ alerts[0].url }}
            tag: varsom_alert
            importance: high
```

## Benefits

✅ **No template sensors needed** - Integration creates both sensors automatically  
✅ **Simple dashboard config** - Just use the filtered sensor directly  
✅ **Always up to date** - Filter changes automatically when you reconfigure  
✅ **Clear separation** - View county-wide OR your area specifically
