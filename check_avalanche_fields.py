#!/usr/bin/env python3
"""Test script to examine avalanche API fields."""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

async def check_avalanche_api_fields():
    """Check what fields are available in avalanche API responses."""
    
    # Use today and tomorrow for the API call
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Get region summary first
    summary_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/RegionSummary/Simple/2/{today}/{tomorrow}"
    
    print("Checking avalanche API fields...")
    print(f"Summary URL: {summary_url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Get region summary
            async with session.get(summary_url) as response:
                if response.status == 200:
                    summary_data = await response.json()
                    
                    if summary_data:
                        print(f"\nFound {len(summary_data)} regions in summary")
                        
                        # Debug first region structure
                        first_region = summary_data[0]
                        print(f"\nFirst region structure:")
                        for key, value in first_region.items():
                            if isinstance(value, (str, int, float)):
                                print(f"  {key}: {value}")
                            else:
                                print(f"  {key}: {type(value).__name__} ({len(value) if hasattr(value, '__len__') else 'N/A'} items)")
                        
                        # Get the first region with warnings for detailed analysis
                        for region in summary_data:
                            avalanche_warnings = region.get("AvalancheWarningList", [])
                            if avalanche_warnings:
                                # Try different possible field names
                                region_id = region.get("RegionId") or region.get("Id") or region.get("regionId")
                                region_name = region.get("RegionName") or region.get("Name") or region.get("regionName")
                                
                                print(f"\nAnalyzing region: {region_name} (ID: {region_id})")
                                
                                # Show warning structure too
                                first_warning = avalanche_warnings[0]
                                print(f"Warning structure:")
                                for key, value in first_warning.items():
                                    if isinstance(value, (str, int, float)):
                                        print(f"  {key}: {value}")
                                    else:
                                        print(f"  {key}: {type(value).__name__}")
                                
                                # Get detailed data for this region
                                detail_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/AvalancheWarningByRegion/Detail/{region_id}/2/{today}/{tomorrow}"
                                
                                async with session.get(detail_url) as detail_response:
                                    if detail_response.status == 200:
                                        detail_data = await detail_response.json()
                                        
                                        if isinstance(detail_data, list) and detail_data:
                                            warning = detail_data[0]  # Examine first warning
                                            
                                            print(f"\nAvailable fields in avalanche warning:")
                                            print("="*50)
                                            
                                            for key, value in warning.items():
                                                if isinstance(value, (str, int, float)):
                                                    print(f"{key}: {value}")
                                                elif isinstance(value, list):
                                                    print(f"{key}: [{len(value)} items] - {type(value[0]).__name__ if value else 'empty'}")
                                                else:
                                                    print(f"{key}: {type(value).__name__}")
                                            
                                            # Show a pretty-printed sample
                                            print(f"\nSample warning data:")
                                            print(json.dumps(warning, indent=2)[:1000] + "...")
                                            
                                            return  # Exit after first example
                                
                                break
                    else:
                        print("No avalanche warnings found")
                else:
                    print(f"Error: HTTP {response.status}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_avalanche_api_fields())