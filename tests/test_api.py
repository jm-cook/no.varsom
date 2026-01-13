"""Unit tests for Norway Alerts API clients."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiohttp import ClientError

from custom_components.norway_alerts.api import (
    LandslideAPI,
    FloodAPI,
    AvalancheAPI,
    MetAlertsAPI,
    WarningAPIFactory,
)


class TestLandslideAPI:
    """Test LandslideAPI client."""

    @pytest.mark.asyncio
    async def test_fetch_warnings_success(self, mock_county_api_response):
        """Test successful fetch of landslide warnings."""
        api = LandslideAPI(county_id="46", county_name="Vestland", lang="en")
        
        # Mock the entire ClientSession to avoid thread creation
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json = AsyncMock(return_value=mock_county_api_response)
            
            # Mock the context managers properly
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock()
            
            mock_session_class.return_value = mock_session
            
            warnings = await api.fetch_warnings()
            
            assert len(warnings) == 1
            assert warnings[0]["_warning_type"] == "landslide"
            assert warnings[0]["ActivityLevel"] == "2"

    @pytest.mark.asyncio
    async def test_fetch_warnings_empty(self):
        """Test fetch when no warnings exist."""
        api = LandslideAPI(county_id="46", county_name="Vestland", lang="en")
        
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json = AsyncMock(return_value=[])
            
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock()
            
            mock_session_class.return_value = mock_session
            
            warnings = await api.fetch_warnings()
            
            assert warnings == []

    @pytest.mark.asyncio
    async def test_fetch_warnings_error(self):
        """Test fetch when API returns error."""
        api = LandslideAPI(county_id="46", county_name="Vestland", lang="en")
        
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 500
            
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock()
            
            mock_session_class.return_value = mock_session
            
            warnings = await api.fetch_warnings()
            
            assert warnings == []


class TestFloodAPI:
    """Test FloodAPI client."""

    @pytest.mark.asyncio
    async def test_fetch_warnings_success(self, mock_county_api_response):
        """Test successful fetch of flood warnings."""
        api = FloodAPI(county_id="46", county_name="Vestland", lang="en")
        
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json = AsyncMock(return_value=mock_county_api_response)
            
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock()
            
            mock_session_class.return_value = mock_session
            
            warnings = await api.fetch_warnings()
            
            assert len(warnings) == 1
            assert warnings[0]["_warning_type"] == "flood"


class TestAvalancheAPI:
    """Test AvalancheAPI client."""

    @pytest.mark.asyncio
    async def test_fetch_warnings_success(self, mock_avalanche_api_response):
        """Test successful fetch of avalanche warnings."""
        api = AvalancheAPI(county_id="46", county_name="Vestland", lang="en")
        
        # Mock summary response
        summary_data = [
            {
                "AvalancheWarningList": [
                    {"RegionId": 3022, "DangerLevel": 3}
                ]
            }
        ]
        
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            
            # First call returns summary
            mock_summary = AsyncMock()
            mock_summary.status = 200
            mock_summary.json = AsyncMock(return_value=summary_data)
            
            # Second call returns details
            mock_detail = AsyncMock()
            mock_detail.status = 200
            mock_detail.json = AsyncMock(return_value=mock_avalanche_api_response)
            
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            
            # Create context manager mocks for get calls
            mock_get_summary = AsyncMock()
            mock_get_summary.__aenter__ = AsyncMock(return_value=mock_summary)
            mock_get_summary.__aexit__ = AsyncMock()
            
            mock_get_detail = AsyncMock()
            mock_get_detail.__aenter__ = AsyncMock(return_value=mock_detail)
            mock_get_detail.__aexit__ = AsyncMock()
            
            mock_session.get.side_effect = [mock_get_summary, mock_get_detail]
            mock_session_class.return_val") as mock_session_class:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json = AsyncMock(return_value=mock_metalerts_api_response)
            
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock()
            
            mock_session_class.return_value = mock_session
            
            warnings = await api.fetch_warnings()
            
            assert len(warnings) == 1
            assert warnings[0]["event"] == "rain"
            assert warnings[0]["ActivityLevel"] == "2"

    @pytest.mark.asyncio
    async def test_fetch_warnings_county(self, mock_metalerts_api_response):
        """Test fetch with county ID."""
        api = MetAlertsAPI(county_id="46", county_name="Vestland", lang="en")
        
        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json = AsyncMock(return_value=mock_metalerts_api_response)
            
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock()
            
            mock_session_class.return_value = mock_session
            
            assert len(warnings) == 1
            assert warnings[0]["event"] == "rain"
            assert warnings[0]["ActivityLevel"] == "2"

    @pytest.mark.asyncio
    async def test_fetch_warnings_county(self, mock_metalerts_api_response):
        """Test fetch with county ID."""
        api = MetAlertsAPI(county_id="46", county_name="Vestland", lang="en")
        
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json = AsyncMock(return_value=mock_metalerts_api_response)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            warnings = await api.fetch_warnings()
            
            assert len(warnings) == 1

    @pytest.mark.asyncio
    async def test_extract_times_from_title(self):
        """Test timestamp extraction from alert title."""
        api = MetAlertsAPI(latitude=60.39, longitude=5.32)
        
        title = "Orange level, 2024-01-01T12:00:00+01:00, 2024-01-02T00:00:00+01:00, Vestland"
        clean_title, start, end = api._extract_times_from_title(title)
        
        assert start == "2024-01-01T12:00:00+01:00"
        assert end == "2024-01-02T00:00:00+01:00"
        assert "Orange level" in clean_title
        assert "2024-01-01T12:00:00+01:00" not in clean_title


class TestWarningAPIFactory:
    """Test WarningAPIFactory."""

    def test_get_landslide_api(self):
        """Test creating landslide API."""
        factory = WarningAPIFactory(county_id="46", county_name="Vestland")
        api = factory.get_api("landslide")
        
        assert isinstance(api, LandslideAPI)
        assert api.county_id == "46"

    def test_get_flood_api(self):
        """Test creating flood API."""
        factory = WarningAPIFactory(county_id="46", county_name="Vestland")
        api = factory.get_api("flood")
        
        assert isinstance(api, FloodAPI)

    def test_get_avalanche_api(self):
        """Test creating avalanche API."""
        factory = WarningAPIFactory(county_id="46", county_name="Vestland")
        api = factory.get_api("avalanche")
        
        assert isinstance(api, AvalancheAPI)

    def test_get_metalerts_api_lat_lon(self):
        """Test creating metalerts API with coordinates."""
        factory = WarningAPIFactory(latitude=60.39, longitude=5.32)
        api = factory.get_api("metalerts")
        
        assert isinstance(api, MetAlertsAPI)
        assert api.latitude == 60.39

    def test_get_metalerts_api_county(self):
        """Test creating metalerts API with county."""
        factory = WarningAPIFactory(county_id="46", county_name="Vestland")
        api = factory.get_api("metalerts")
        
        assert isinstance(api, MetAlertsAPI)
        assert api.county_id == "46"

    def test_unknown_warning_type(self):
        """Test with unknown warning type."""
        factory = WarningAPIFactory(county_id="46", county_name="Vestland")
        
        with pytest.raises(ValueError, match="Unknown warning type"):
            factory.get_api("unknown")
