#!/usr/bin/env python3
"""Script to analyze avalanche-specific attributes vs generic warning attributes."""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

async def analyze_avalanche_attributes():
    """Compare avalanche-specific vs generic warning attributes."""
    
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Get region summary first
    summary_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/RegionSummary/Simple/2/{today}/{tomorrow}"
    
    print("Analyzing avalanche API attributes...")
    print("=" * 60)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(summary_url) as response:
                if response.status != 200:
                    print(f"Error: HTTP {response.status}")
                    return
                    
                summary_data = await response.json()
                if not summary_data:
                    print("No avalanche warnings found")
                    return
                
                print(f"Found {len(summary_data)} regions\n")
                
                # Find regions with active warnings
                active_regions = []
                for region in summary_data:
                    warnings = region.get("AvalancheWarningList", [])
                    for warning in warnings:
                        danger_level = warning.get('DangerLevel', 0)
                        # Handle both string and int danger levels
                        try:
                            if isinstance(danger_level, str):
                                danger_level = int(danger_level)
                            if danger_level > 0:
                                active_regions.append((region, warning))
                        except (ValueError, TypeError):
                            pass
                
                if active_regions:
                    print(f"Found {len(active_regions)} regions with active warnings")
                    region, warning = active_regions[0]
                    region_id = region['Id']
                    region_name = region['Name']
                    print(f"Analyzing: {region_name} (Danger Level: {warning.get('DangerLevel')})")
                else:
                    # Use first region regardless
                    region = summary_data[0]
                    region_id = region['Id']
                    region_name = region['Name']
                    print(f"No active warnings, analyzing: {region_name}")
                
                # Get detailed data for this region
                detail_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/AvalancheWarningByRegion/Detail/{region_id}/2/{today}/{tomorrow}"
                
                async with session.get(detail_url) as detail_response:
                    if detail_response.status != 200:
                        print(f"Error getting details: HTTP {detail_response.status}")
                        return
                        
                    detail_data = await detail_response.json()
                    
                    if not isinstance(detail_data, list) or not detail_data:
                        print("No detailed warning data available")
                        return
                    
                    warning = detail_data[0]
                    
                    print("\nCURRENT GENERIC ATTRIBUTES (used by floods/landslides):")
                    print("-" * 50)
                    
                    generic_fields = ['warning_text', 'advice_text', 'consequence_text']
                    # These don't exist in avalanche API - we would need to map them
                    print("❌ warning_text - NOT AVAILABLE in avalanche API")
                    print("❌ advice_text - NOT AVAILABLE in avalanche API") 
                    print("❌ consequence_text - NOT AVAILABLE in avalanche API")
                    
                    print("\nAVALANCHE-SPECIFIC ATTRIBUTES AVAILABLE:")
                    print("-" * 50)
                    
                    avalanche_fields = {
                        'MainText': 'Primary warning message',
                        'AvalancheDanger': 'Detailed avalanche danger description',
                        'EmergencyWarning': 'Emergency warning text (if applicable)',
                        'AvalancheProblems': 'Specific avalanche problem types',
                        'AvalancheAdvices': 'Avalanche-specific safety advice',
                        'SnowSurface': 'Current snow surface conditions', 
                        'CurrentWeaklayers': 'Weak layers in snow pack',
                        'LatestAvalancheActivity': 'Recent avalanche observations',
                        'LatestObservations': 'Latest field observations',
                        'MountainWeather': 'Mountain weather impact',
                        'ExposedHeight1': 'Elevation where danger applies',
                        'ExposedHeightFill': 'Elevation range details',
                        'Author': 'Forecaster who issued warning',
                        'DangerLevelName': 'Human-readable danger level'
                    }
                    
                    available_fields = []
                    unavailable_fields = []
                    
                    for field, description in avalanche_fields.items():
                        value = warning.get(field)
                        if value is not None and value != "" and value != 0:
                            available_fields.append(field)
                            print(f"✓ {field}: {description}")
                            if isinstance(value, (list, dict)):
                                print(f"  Type: {type(value).__name__}, Size: {len(value)}")
                                if isinstance(value, list) and value:
                                    print(f"  Sample item: {type(value[0]).__name__}")
                            else:
                                sample = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                                print(f"  Value: {sample}")
                        else:
                            unavailable_fields.append(field)
                            print(f"✗ {field}: {description} (empty/null)")
                    
                    print(f"\nSUMMARY:")
                    print("-" * 50)
                    print(f"Available avalanche fields: {len(available_fields)}")
                    print(f"Unavailable avalanche fields: {len(unavailable_fields)}")
                    
                    print(f"\nRECOMMENDATION:")
                    print("-" * 50)
                    print("Replace generic warning attributes with avalanche-specific ones:")
                    
                    if warning.get('MainText'):
                        print("• Use 'MainText' instead of 'warning_text'")
                    if warning.get('AvalancheAdvices'):
                        print("• Use 'AvalancheAdvices' instead of 'advice_text'")
                    if warning.get('AvalancheDanger'):
                        print("• Use 'AvalancheDanger' instead of 'consequence_text'")
                        
                    # Show sample data for key fields
                    print(f"\nSAMPLE DATA FOR KEY FIELDS:")
                    print("-" * 50)
                    key_fields = ['MainText', 'AvalancheDanger', 'AvalancheAdvices', 'AvalancheProblems']
                    for field in key_fields:
                        value = warning.get(field)
                        if value:
                            print(f"{field}:")
                            if isinstance(value, (list, dict)):
                                print(json.dumps(value, indent=2, ensure_ascii=False)[:300] + "...")
                            else:
                                print(f"  {str(value)[:200]}...")
                            print()
                    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(analyze_avalanche_attributes())