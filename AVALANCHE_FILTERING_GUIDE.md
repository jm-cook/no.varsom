# Individual Alert Icons Usage

With the latest update, each alert now includes an `entity_picture` field containing the appropriate warning icon. This allows you to display individual icons for each alert in markdown templates.

## Example Markdown Template

```jinja2
## Weather Alerts for {{ state_attr('sensor.varsom_avalanche_vestland', 'county_name') }}

{% set alerts = state_attr('sensor.varsom_avalanche_vestland', 'alerts') %}
{% if alerts and alerts|length > 0 %}
**Active Alerts: {{ alerts|length }}** | **Highest Level: {{ state_attr('sensor.varsom_avalanche_vestland', 'highest_level')|title }}**

{% for alert in alerts -%}
### {% if alert.entity_picture %}<img src="{{ alert.entity_picture }}" width="24" height="24" style="vertical-align: middle;">{% endif %} {{ alert.region_name or 'Alert' }} - {{ alert.level_name|title }}

**Municipalities:** {{ alert.municipalities|join(', ') }}  
**Valid:** {{ alert.valid_from[:10] }} to {{ alert.valid_to[:10] }}  
**Warning:** {{ alert.main_text }}

{% if alert.url %}[View Details →]({{ alert.url }}){% endif %}

---
{% endfor %}
{% else %}
✅ No active weather warnings
{% endif %}
```

## Key Improvements

### 1. Better Regional Filtering
- **Relevance Score:** Only includes avalanche regions where ≥30% of municipalities are in your county
- **Reduced Noise:** Filters out regions that barely touch your county boundary
- **Smart Filtering:** Vestland sensors should now only show truly relevant regions like:
  - ✅ Voss (clearly in Vestland)
  - ✅ Hardanger (clearly in Vestland)  
  - ✅ Indre Sogn (clearly in Vestland)
  - ❌ Sunnmøre (mainly Møre og Romsdal)
  - ❌ Hallingdal (mainly Viken)
  - ❌ Vest-Telemark (mainly Telemark)

### 2. Individual Alert Icons
- **Per-Alert Icons:** Each alert has its own `entity_picture` field
- **Automatic Selection:** Icons automatically match the alert's warning type and level
- **Markdown Ready:** Direct URL for use in markdown templates and cards
- **Responsive Design:** 48x48px SVG icons scale perfectly at any size

## Expected Results

Your Vestland avalanche sensor should now show:
- **Fewer, more relevant regions** (probably 4-6 instead of 9)
- **Individual icons** for each alert that you can use in templates
- **Better geographic accuracy** for your specific county

The filtering should eliminate the cross-county regions that were showing up before!