#!/usr/bin/env python3
"""Simple test of avalanche attributes."""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

async def test_avalanche_attributes():
    """Test avalanche-specific attributes."""
    
    print("Testing avalanche-specific attributes from live API...")
    print("=" * 60)
    
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Get Vestland county ID 46
    summary_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/RegionSummary/Simple/2/{today}/{tomorrow}"
    
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
                
                # Find a region with active warnings relevant to Vestland
                vestland_warnings = []
                for region in summary_data:
                    warnings = region.get("AvalancheWarningList", [])
                    for warning in warnings:
                        danger_level = warning.get('DangerLevel', 0)
                        if isinstance(danger_level, str):
                            danger_level = int(danger_level) if danger_level.isdigit() else 0
                        if danger_level > 0:
                            # Get detailed data
                            region_id = region['Id']
                            detail_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/AvalancheWarningByRegion/Detail/{region_id}/2/{today}/{tomorrow}"
                            
                            async with session.get(detail_url) as detail_response:
                                if detail_response.status == 200:
                                    detail_data = await detail_response.json()
                                    if isinstance(detail_data, list) and detail_data:
                                        detail_warning = detail_data[0]
                                        # Check if this region has municipalities in Vestland
                                        municipalities = detail_warning.get("MunicipalityList", [])
                                        for muni in municipalities:
                                            if muni.get("CountyId") == "46" or str(muni.get("CountyId")) == "46":
                                                vestland_warnings.append(detail_warning)
                                                break
                                        if len(vestland_warnings) >= 1:  # Just get one example
                                            break
                            break
                    if vestland_warnings:
                        break
                
                if vestland_warnings:
                    print(f"Found avalanche warnings relevant to Vestland\n")
                    
                    # Examine first warning
                    warning = vestland_warnings[0]
        
        print(f"Region: {warning.get('RegionName', 'N/A')}")
        print(f"Danger Level: {warning.get('DangerLevel', 'N/A')}")
        print(f"Warning Type: {warning.get('_warning_type', 'N/A')}")
        print()
        
        print("AVALANCHE-SPECIFIC ATTRIBUTES:")
        print("-" * 40)
        
        avalanche_fields = {
            'MainText': 'Main warning message',
            'AvalancheDanger': 'Detailed danger description',
            'EmergencyWarning': 'Emergency warning',
            'AvalancheProblems': 'Problem types',
            'AvalancheAdvices': 'Safety advice',
            'SnowSurface': 'Snow surface conditions',
            'CurrentWeaklayers': 'Weak layers',
            'LatestAvalancheActivity': 'Recent activity',
            'LatestObservations': 'Latest observations',
            'MountainWeather': 'Weather conditions',
            'Author': 'Forecaster',
            'DangerLevelName': 'Danger level name',
            'ExposedHeight1': 'Exposed elevation',
            'ExposedHeightFill': 'Elevation range'
        }
        
        for field, description in avalanche_fields.items():
            value = warning.get(field)
            if value:
                if isinstance(value, str):
                    sample = value[:80] + "..." if len(value) > 80 else value
                    print(f"✓ {field}: {sample}")
                elif isinstance(value, list):
                    print(f"✓ {field}: [{len(value)} items]")
                    if value and isinstance(value[0], dict):
                        print(f"    Sample keys: {list(value[0].keys())}")
                elif isinstance(value, dict):
                    print(f"✓ {field}: dict with {len(value)} keys")
                    print(f"    Keys: {list(value.keys())}")
                else:
                    print(f"✓ {field}: {value}")
            else:
                print(f"✗ {field}: (empty)")
                else:
                    print("No avalanche warnings found relevant to Vestland")
                    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
if __name__ == "__main__":
    asyncio.run(test_avalanche_attributes())