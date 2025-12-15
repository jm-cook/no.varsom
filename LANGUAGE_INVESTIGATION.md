# Language Support Investigation Results

**Date**: December 15, 2025

## Problem Reported

User reported that regardless of language selection (Norwegian or English), they always received:
- Norwegian alert text
- English URLs to Varsom.no

## Initial Investigation (INCORRECT)

Initially tested URL path suffixes `/no` and `/en`, which both returned Norwegian text.

## Correct Solution (Updated)

User pointed to the Swagger documentation which indicated the format:
`/Warning/{Språknøkkel}/{Startdato}/{Sluttdato}`

After testing various combinations, found the correct format for county-based warnings:

### Correct API URL Format

**`/Warning/County/{CountyId}/{Språknøkkel}`**

Where Språknøkkel is:
- **`1`** = Norwegian (returns LangKey: 1)
- **`2`** = English (returns LangKey: 2)

### Test Results

| URL Format | Status | LangKey | DangerTypeName | MainText |
|-----------|--------|---------|----------------|----------|
| `.../County/46/1` | 200 | 1 | "Jord- og flomskredfare" | "Varsel om jord- og flomskredfare..." (Norwegian) |
| `.../County/46/2` | 200 | 2 | "Debris avalanches and debris flows" | "Debris avalanches and debris flows warning..." (English) |

The alerts are **NOT identical** - English version (LangKey: 2) returns English text!

## Varsom.no URL Testing

Tested both URL formats:
- `https://www.varsom.no/en/flood-and-landslide-warning-service/forecastid/584732` → **200 OK** ✅
- `https://www.varsom.no/flood-and-landslide-warning-service/forecastid/584732` → **200 OK** ✅

Both work! The `/en/` prefix switches the Varsom.no website interface to English.

## Code Changes Made

### 1. Fixed API URL Construction
**File**: `custom_components/varsom/sensor.py`

Changed from:
```python
url = f"{base_url}/Warning/County/{self.county_id}/no"  # WRONG - always Norwegian
```

To:
```python
# NVE API uses Språknøkkel (language key) as path parameter:
# 1 = Norwegian (LangKey: 1), 2 = English (LangKey: 2)
lang_key = "2" if self.lang == "en" else "1"
url = f"{base_url}/Warning/County/{self.county_id}/{lang_key}"  # CORRECT
```

**Impact**: API now correctly returns Norwegian or English text based on user's language selection.

### 2. Kept Varsom.no URL Construction
**File**: `custom_components/varsom/sensor.py` (Line 289)

```python
lang_path = "en" if self.coordinator.lang == "en" else ""
varsom_url = f"https://www.varsom.no/{lang_path}/flood-and-landslide-warning-service/forecastid/{url_id}".replace("//f", "/f")
```

**Why keep it**: The language setting correctly controls whether Varsom.no links use the English or Norwegian website interface.

### 3. Updated Documentation
**File**: `README.md`

Updated section to correctly explain language support:

```markdown
### Language Support

The language option you select during setup controls both:
- ✅ The alert text language (Norwegian or English from the API via Språknøkkel parameter)
- ✅ The language of the Varsom.no website links (Norwegian or English interface)

The API uses the Språknøkkel path parameter:
- `1` = Norwegian (LangKey: 1 in response)
- `2` = English (LangKey: 2 in response)
```

## Expected Behavior After Fix

| Setting | API Text | Varsom.no URL | Varsom.no Interface |
|---------|----------|---------------|---------------------|
| Norwegian | Norwegian 🇳🇴 | `varsom.no/flood-and-landslide...` | Norwegian 🇳🇴 |
| English | **English 🇬🇧** | `varsom.no/en/flood-and-landslide...` | English 🇬🇧 |

## Additional Notes

- The `LangKey` field in API responses is `1` for Norwegian, `2` for English
- The Språknøkkel parameter MUST be a path parameter, not a query parameter
- English translations include field names like "Debris avalanches and debris flows" instead of "Jord- og flomskredfare"
- The API has full English support when using Språknøkkel=2

## Files Modified

1. `custom_components/varsom/sensor.py` - Fixed API URL to use Språknøkkel (1 or 2)
2. `README.md` - Updated language support documentation to reflect correct behavior
3. `LANGUAGE_INVESTIGATION.md` - Updated this file with correct solution
4. Test scripts created: `test_language_options.py`, `test_spraknokkel.py`, `test_url_formats.py` (can be deleted)

## Testing Recommendation

To verify the fix:
1. Reload the integration in Home Assistant
2. Check that alert text is in Norwegian (expected)
3. Check that Varsom.no URLs work and show correct language interface
4. If English was selected, URLs should have `/en/` prefix
5. If Norwegian was selected, URLs should NOT have `/en/` prefix
