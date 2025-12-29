"""
NASA API Integration Services
Handles fetching, parsing, and caching data from all 16 NASA APIs
"""
import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging
from functools import lru_cache
import redis
import json

logger = logging.getLogger(__name__)


class NASAAPIBase:
    """Base class for NASA API services with common functionality."""
    
    def __init__(self, api_key: str, redis_client: Optional[redis.Redis] = None):
        self.api_key = api_key
        self.redis = redis_client
        self.cache_ttl = 86400  # 24 hours default
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    async def fetch(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Fetch data from API with retry logic and caching."""
        if not params:
            params = {}
        params['api_key'] = self.api_key
        
        # Check cache
        cache_key = f"{self.__class__.__name__}:{url}:{json.dumps(params, sort_keys=True)}"
        if self.redis:
            cached = self.redis.get(cache_key)
            if cached:
                logger.info(f"Cache hit for {cache_key}")
                return json.loads(cached)
        
        # Fetch with retry
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Cache result
                            if self.redis:
                                self.redis.setex(
                                    cache_key,
                                    self.cache_ttl,
                                    json.dumps(data, default=str)
                                )
                            return data
                        elif response.status == 429:  # Rate limited
                            logger.warning(f"Rate limited, retrying in {self.retry_delay}s")
                            await asyncio.sleep(self.retry_delay)
                        else:
                            logger.error(f"API error {response.status}: {await response.text()}")
                            return None
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
            except Exception as e:
                logger.error(f"Fetch error: {str(e)}")
                return None
        
        return None


class APODService(NASAAPIBase):
    """Astronomy Picture of the Day API"""
    BASE_URL = "https://api.nasa.gov/planetary/apod"
    
    async def get_apod(self, date: Optional[str] = None, count: int = 1) -> Optional[Dict]:
        """Get APOD for specific date or latest."""
        params = {}
        if date:
            params['date'] = date
        else:
            params['count'] = count
        
        data = await self.fetch(self.BASE_URL, params)
        return data
    
    async def get_apod_range(self, start_date: str, end_date: str) -> Optional[List[Dict]]:
        """Get APOD for date range."""
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        return await self.fetch(self.BASE_URL, params)


class AsteroidsNeoWSService(NASAAPIBase):
    """Asteroids NeoWs - Near Earth Object Web Service"""
    BASE_URL = "https://api.nasa.gov/neo/rest/v1/neo"
    BROWSE_URL = "https://api.nasa.gov/neo/rest/v1/neo/browse"
    
    async def get_asteroid_by_id(self, neo_id: str) -> Optional[Dict]:
        """Get specific asteroid data."""
        url = f"{self.BASE_URL}/{neo_id}"
        return await self.fetch(url)
    
    async def get_asteroids_today(self) -> Optional[Dict]:
        """Get asteroids for today."""
        url = "https://api.nasa.gov/neo/rest/v1/feed/today"
        return await self.fetch(url)
    
    async def get_asteroids_by_date(self, start_date: str, end_date: str) -> Optional[Dict]:
        """Get asteroids for date range."""
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        return await self.fetch(url, params)
    
    async def browse_asteroids(self, page: int = 0) -> Optional[Dict]:
        """Browse all asteroids paginated."""
        params = {'page': page}
        return await self.fetch(self.BROWSE_URL, params)


class DONKIService(NASAAPIBase):
    """DONKI - Space Weather Events & Alerts"""
    BASE_URL = "https://api.nasa.gov/DONKI"
    
    async def get_flare_events(self, start_date: str, end_date: Optional[str] = None) -> Optional[List]:
        """Get solar flare events."""
        url = f"{self.BASE_URL}/FLR"
        params = {'startDate': start_date}
        if end_date:
            params['endDate'] = end_date
        return await self.fetch(url, params)
    
    async def get_sep_events(self, start_date: str, end_date: Optional[str] = None) -> Optional[List]:
        """Get solar energetic particle events."""
        url = f"{self.BASE_URL}/SEP"
        params = {'startDate': start_date}
        if end_date:
            params['endDate'] = end_date
        return await self.fetch(url, params)
    
    async def get_mpc_events(self, start_date: str, end_date: Optional[str] = None) -> Optional[List]:
        """Get magnetopause crossing events."""
        url = f"{self.BASE_URL}/MPC"
        params = {'startDate': start_date}
        if end_date:
            params['endDate'] = end_date
        return await self.fetch(url, params)
    
    async def get_rbe_events(self, start_date: str, end_date: Optional[str] = None) -> Optional[List]:
        """Get radiation belt enhancement events."""
        url = f"{self.BASE_URL}/RBE"
        params = {'startDate': start_date}
        if end_date:
            params['endDate'] = end_date
        return await self.fetch(url, params)
    
    async def get_hss_events(self, start_date: str, end_date: Optional[str] = None) -> Optional[List]:
        """Get high speed stream events."""
        url = f"{self.BASE_URL}/HSS"
        params = {'startDate': start_date}
        if end_date:
            params['endDate'] = end_date
        return await self.fetch(url, params)
    
    async def get_cme_events(self, start_date: str, end_date: Optional[str] = None) -> Optional[List]:
        """Get coronal mass ejection events."""
        url = f"{self.BASE_URL}/CME"
        params = {'startDate': start_date}
        if end_date:
            params['endDate'] = end_date
        return await self.fetch(url, params)


class EONETService(NASAAPIBase):
    """EONET - Earth Observation Natural Events Tracking"""
    BASE_URL = "https://eonet.gsfc.nasa.gov/api/v3"
    
    async def get_events(self, status: Optional[str] = None, limit: int = 10) -> Optional[Dict]:
        """Get natural events."""
        url = f"{self.BASE_URL}/events"
        params = {'limit': limit}
        if status:
            params['status'] = status
        # EONET doesn't use NASA API key
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_event_by_id(self, event_id: str) -> Optional[Dict]:
        """Get specific event."""
        url = f"{self.BASE_URL}/events/{event_id}"
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_categories(self) -> Optional[Dict]:
        """Get event categories."""
        url = f"{self.BASE_URL}/categories"
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        return None


class EPICService(NASAAPIBase):
    """EPIC - Earth Polychromatic Imaging Camera"""
    BASE_URL = "https://api.nasa.gov/EPIC/api/natural"
    IMAGERY_URL = "https://api.nasa.gov/EPIC/api/natural/imagery"
    
    async def get_imagery(self, date: Optional[str] = None) -> Optional[List]:
        """Get Earth imagery for date."""
        url = self.BASE_URL
        params = {}
        if date:
            url = f"{url}/date/{date}"
        else:
            url = f"{url}/available"
        return await self.fetch(url, params)
    
    async def get_image_url(self, date: str, image_name: str) -> str:
        """Build EPIC image URL."""
        parts = image_name.split('_')
        return f"https://api.nasa.gov/EPIC/archive/natural/{date.replace('-', '/')}/png/{image_name}.png"


class ExoplanetService(NASAAPIBase):
    """Exoplanet Archive - Confirmed Exoplanets"""
    BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    
    async def query_exoplanets(self, query: str) -> Optional[Dict]:
        """Query exoplanet database using ADQL."""
        params = {
            'query': query,
            'format': 'json'
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_habitable_exoplanets(self) -> Optional[Dict]:
        """Get exoplanets in habitable zone."""
        query = "SELECT pl_name, hostname, pl_period, pl_semimajor_axis, st_teff FROM ps_default WHERE pl_disc_year > 2000 AND pl_insol > 0.2 AND pl_insol < 2"
        return await self.query_exoplanets(query)


class GIBSService(NASAAPIBase):
    """GIBS - Global Imagery Browse Services"""
    BASE_URL = "https://map1.vis.earthdata.nasa.gov/wmts-webmerc"
    
    async def get_layer_info(self, layer: str, date: str = None) -> Optional[str]:
        """Get GIBS layer info."""
        params = {
            'layer': layer,
            'tilematrixset': 'GoogleMapsCompatible_Level8',
            'Service': 'WMTS',
            'Request': 'GetCapabilities'
        }
        if date:
            params['time'] = date
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(f"{self.BASE_URL}/1.0.0/WMTSCapabilities.xml", params=params) as response:
                if response.status == 200:
                    return await response.text()
        return None
    
    def get_tile_url(self, layer: str, date: str, x: int, y: int, z: int) -> str:
        """Build GIBS tile URL."""
        return f"{self.BASE_URL}/1.0.0/{layer}/default/{date}/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpg"


class InSightWeatherService(NASAAPIBase):
    """InSight Mars Weather - Sol-by-sol data"""
    BASE_URL = "https://api.nasa.gov/insight_as_service/activity"
    
    async def get_latest_weather(self) -> Optional[Dict]:
        """Get latest Mars weather."""
        return await self.fetch(self.BASE_URL)
    
    async def get_weather_by_sol(self, sol: int) -> Optional[Dict]:
        """Get weather for specific Martian day."""
        url = f"{self.BASE_URL}/{sol}"
        return await self.fetch(url)


class NASAImageLibraryService(NASAAPIBase):
    """NASA Image & Video Library"""
    BASE_URL = "https://images-api.nasa.gov/search"
    
    async def search_images(self, query: str, limit: int = 10) -> Optional[Dict]:
        """Search NASA image library."""
        params = {
            'q': query,
            'page_size': limit,
            'media_type': 'image'
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def search_videos(self, query: str, limit: int = 10) -> Optional[Dict]:
        """Search NASA video library."""
        params = {
            'q': query,
            'page_size': limit,
            'media_type': 'video'
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None


class OpenScienceService(NASAAPIBase):
    """Open Science Data Repository"""
    BASE_URL = "https://api.osis.nasa.gov/data"
    
    async def search_datasets(self, query: str, limit: int = 10) -> Optional[Dict]:
        """Search open science datasets."""
        params = {
            'query': query,
            'limit': limit
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """Get specific dataset."""
        url = f"{self.BASE_URL}/{dataset_id}"
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        return None


class SatelliteSituationCenterService(NASAAPIBase):
    """Satellite Situation Center - Active Satellites"""
    BASE_URL = "https://api.nasa.gov/asset/asset/query"
    
    async def get_satellites(self, limit: int = 100) -> Optional[Dict]:
        """Get active satellites."""
        params = {
            'query': {
                'filter': [
                    {
                        'name': 'operational_status',
                        'operation': '==',
                        'value': 'operational'
                    }
                ],
                'limit': limit
            }
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(self.BASE_URL, json=params) as response:
                if response.status == 200:
                    return await response.json()
        return None


class CNEOSService(NASAAPIBase):
    """CNEOS - Center for Near Earth Object Studies (Planetary Defense)"""
    BASE_URL = "https://api.nasa.gov/ssd/api/cad.api"
    
    async def query_close_approaches(self, start_date: str, end_date: str) -> Optional[Dict]:
        """Query close approach data."""
        params = {
            'date-min': start_date,
            'date-max': end_date,
            'limit': 1000,
            'sort': 'date'
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None


class TechPortService(NASAAPIBase):
    """TechPort - NASA Technology Projects"""
    BASE_URL = "https://api.nasa.gov/techport/api/projects"
    
    async def get_projects(self, limit: int = 50) -> Optional[Dict]:
        """Get NASA tech projects."""
        params = {
            'format': 'json',
            'limit': limit
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_project(self, project_id: str) -> Optional[Dict]:
        """Get specific project."""
        url = f"{self.BASE_URL}/{project_id}"
        params = {'format': 'json'}
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None


class TechTransferService(NASAAPIBase):
    """TechTransfer - NASA Spinoff Technologies"""
    BASE_URL = "https://api.nasa.gov/techtransfer/spinoff"
    
    async def get_spinoffs(self, limit: int = 50) -> Optional[Dict]:
        """Get NASA spinoff technologies."""
        params = {'format': 'json', 'limit': limit}
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_spinoff(self, spinoff_id: str) -> Optional[Dict]:
        """Get specific spinoff."""
        url = f"{self.BASE_URL}/{spinoff_id}"
        params = {'format': 'json'}
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None


class TLEService(NASAAPIBase):
    """TLE API - Satellite Tracking (Two-Line Elements)"""
    BASE_URL = "https://api.nasa.gov/ssd_svn/rss_feeds/tle.php"
    
    async def get_tle_for_satellite(self, satellite_id: str) -> Optional[Dict]:
        """Get TLE for satellite."""
        params = {
            'CATNR': satellite_id,
            'FORMAT': 'json'
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None
    
    async def get_tle_by_name(self, satellite_name: str) -> Optional[Dict]:
        """Get TLE by satellite name."""
        params = {
            'SATNAME': satellite_name,
            'FORMAT': 'json'
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
        return None


class TrekWMSService(NASAAPIBase):
    """Trek WMS - Vesta, Moon, Mars Imagery (Web Map Service)"""
    BASE_URL = "https://trek.gsfc.nasa.gov/tiles/Moon/SRTM30_PLUS/default//Moon_SRTM30_PLUS_srtm.vrt.xml"
    
    async def get_wms_capabilities(self, body: str = "Moon") -> Optional[str]:
        """Get WMS capabilities for celestial body."""
        # Different endpoints for different bodies
        urls = {
            "Moon": "https://trek.gsfc.nasa.gov/tiles/Moon/SRTM30_PLUS/default//Moon_SRTM30_PLUS_srtm.vrt.xml",
            "Mars": "https://trek.gsfc.nasa.gov/tiles/Mars/MOLA/default//Mars_MOLA_srtm.vrt.xml",
            "Vesta": "https://trek.gsfc.nasa.gov/tiles/Vesta/DEM/default//Vesta_DEM_srtm.vrt.xml"
        }
        url = urls.get(body, urls["Moon"])
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        return None
    
    def get_tile_url(self, body: str, layer: str, z: int, x: int, y: int) -> str:
        """Build Trek tile URL."""
        return f"https://trek.gsfc.nasa.gov/tiles/{body}/{layer}/default/{z}/{x}/{y}.png"
