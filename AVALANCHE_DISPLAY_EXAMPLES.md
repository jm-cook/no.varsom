# Avalanche Warning Display Examples

This document shows how to display the rich avalanche-specific attributes in Home Assistant cards and templates, which differs significantly from the simple landslide/flood warning displays.

## Simple Display Template

For a basic avalanche warning card:

```yaml
type: markdown
content: >
  ## 🏔️ Avalanche Warning: {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].region_name }}
  
  **Danger Level:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].danger_level_name }}  
  **Valid:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].valid_from | as_timestamp | timestamp_custom('%d/%m %H:%M') }} - {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].valid_to | as_timestamp | timestamp_custom('%d/%m %H:%M') }}
  
  ### Main Warning
  {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].main_text }}
  
  ### Current Conditions
  **Snow Surface:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].snow_surface | truncate(150) }}
  
  **Weak Layers:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].current_weaklayers | truncate(150) }}
  
  ---
  *Issued by: {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].forecaster }}*
```

## Detailed Display Template

For a comprehensive avalanche information display:

```yaml
type: markdown
content: >
  # 🏔️ {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].region_name }}
  
  ## {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].danger_level_name }}
  
  **Valid Period:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].valid_from | as_timestamp | timestamp_custom('%A %d %B, %H:%M') }} - {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].valid_to | as_timestamp | timestamp_custom('%A %d %B, %H:%M') }}
  
  ### 📢 Main Warning
  {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].main_text }}
  
  {% if states.sensor.varsom_avalanche_vestland.attributes.alerts[0].emergency_warning %}
  ### 🚨 Emergency Warning  
  {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].emergency_warning }}
  {% endif %}
  
  ### ⚡ Avalanche Danger Assessment
  {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_danger }}
  
  ### ❄️ Snow Conditions
  **Surface:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].snow_surface }}
  
  **Weak Layers:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].current_weaklayers }}
  
  ### 📊 Recent Activity & Observations
  {% if states.sensor.varsom_avalanche_vestland.attributes.alerts[0].latest_avalanche_activity %}
  **Recent Avalanches:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].latest_avalanche_activity }}
  {% endif %}
  
  **Field Observations:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].latest_observations }}
  
  ### 🎯 Avalanche Problems
  {% for problem in states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_problems %}
  **Problem {{ loop.index }}:** {{ problem.AvalancheExtName }}  
  **Cause:** {{ problem.AvalCauseName }}  
  **Probability:** {{ problem.AvalProbabilityName }}  
  **Trigger:** {{ problem.AvalTriggerSimpleName }}  
  {% if problem.AvalancheExtName == "Dry slab avalanche" %}🎿{% elif problem.AvalancheExtName == "Wet avalanche" %}💧{% else %}⚠️{% endif %}
  {% endfor %}
  
  ### 🛡️ Safety Advice
  {% for advice in states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_advices %}
  **{{ loop.index }}.** {{ advice.Text }}
  {% if advice.ImageUrl %}
  ![Safety advice]({{ advice.ImageUrl }})
  {% endif %}
  {% endfor %}
  
  ### 🌤️ Mountain Weather Impact
  {% set weather = states.sensor.varsom_avalanche_vestland.attributes.alerts[0].mountain_weather %}
  {% if weather %}
  **Wind:** {{ weather.WindSpeed }} {{ weather.WindDirection }}  
  **Temperature:** {{ weather.Temperature }}°C  
  **Precipitation:** {{ weather.Precipitation }}
  {% endif %}
  
  ---
  **Elevation:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].exposed_height }}m+  
  **Forecaster:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].forecaster }}  
  **Region ID:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].region_id }}
```

## Comparison: Landslide vs Avalanche Display

### Landslide/Flood Warning (Simple)
```yaml
content: >
  ## 🌊 Flood Warning: {{ states.sensor.varsom_flood_vestland.attributes.alerts[0].area_name }}
  
  **Level:** {{ states.sensor.varsom_flood_vestland.attributes.alerts[0].danger_level }}
  
  ### Warning
  {{ states.sensor.varsom_flood_vestland.attributes.alerts[0].warning_text }}
  
  ### Advice  
  {{ states.sensor.varsom_flood_vestland.attributes.alerts[0].advice_text }}
  
  ### Consequences
  {{ states.sensor.varsom_flood_vestland.attributes.alerts[0].consequence_text }}
```

### Avalanche Warning (Rich Data)
```yaml
content: >
  ## 🏔️ Avalanche Warning: {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].region_name }}
  
  **Level:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].danger_level_name }}
  
  ### Main Warning
  {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].main_text }}
  
  ### Technical Assessment
  {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_danger }}
  
  ### Snow Analysis
  **Surface:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].snow_surface | truncate(100) }}
  **Weak Layers:** {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].current_weaklayers | truncate(100) }}
  
  ### Problems ({{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_problems | length }})
  {% for problem in states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_problems %}
  • **{{ problem.AvalancheExtName }}** ({{ problem.AvalProbabilityName }})
  {% endfor %}
  
  ### Safety Advice ({{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_advices | length }})
  {% for advice in states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_advices %}
  {{ loop.index }}. {{ advice.Text }}
  {% endfor %}
```

## Dashboard Card Examples

### Compact Avalanche Card
```yaml
type: entities
title: Current Avalanche Conditions
entities:
  - entity: sensor.varsom_avalanche_vestland
    type: custom:template-entity-row
    name: "{{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].region_name }}"
    secondary: "{{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].danger_level_name }}"
    icon: "{{ states.sensor.varsom_avalanche_vestland.attributes.entity_picture }}"
```

### Avalanche Problem Summary
```yaml
type: markdown
title: Avalanche Problems Today
content: >
  {% for problem in states.sensor.varsom_avalanche_vestland.attributes.alerts[0].avalanche_problems %}
  ### {{ problem.AvalancheExtName }}
  **Cause:** {{ problem.AvalCauseName }}  
  **Likelihood:** {{ problem.AvalProbabilityName }}  
  **Triggering:** {{ problem.AvalTriggerSimpleName }}
  
  {% endfor %}
```

### Mountain Conditions Card
```yaml
type: vertical-stack
cards:
  - type: markdown
    content: >
      ## ❄️ Current Snow Conditions
      {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].snow_surface }}
      
      ## 🔍 Weak Layers Analysis  
      {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].current_weaklayers }}
      
      ## 📊 Recent Activity
      {{ states.sensor.varsom_avalanche_vestland.attributes.alerts[0].latest_observations }}
```

## Key Differences from Landslide/Flood

1. **Structured Data**: Avalanche warnings have arrays of problems and advice vs simple text fields
2. **Technical Detail**: Snow analysis, weak layers, and mountain weather vs generic consequences  
3. **Visual Elements**: Advice includes images and icons vs plain text
4. **Professional Terminology**: Uses avalanche-specific terms and danger scale
5. **Multiple Information Sources**: Problems, observations, weather impact vs single warning text

The avalanche display templates can leverage this rich structured data to provide much more useful and actionable information for backcountry users compared to the generic warning text used by landslide and flood warnings.