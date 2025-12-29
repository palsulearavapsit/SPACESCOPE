"""
NASA API Ingestion Tasks for Celery
Background jobs for fetching and storing NASA data
"""
from celery import shared_task
from datetime import datetime, timedelta
import logging
from sqlalchemy import select
from app.db import async_session_maker
from app.models.db_models import (
    APOD, AsteroidNeoWS, DONKI, EONET, EPIC, Exoplanet, GIBS,
    InSightWeather, NASAImageLibrary, OpenScience, SatelliteSituationCenter,
    CNEOS, TechPort, TechTransfer, TLE, TrekWMS
)
from app.services.nasa_apis import (
    APODService, AsteroidsNeoWSService, DONKIService, EONETService,
    EPICService, ExoplanetService, GIBSService, InSightWeatherService,
    NASAImageLibraryService, OpenScienceService, SatelliteSituationCenterService,
    CNEOSService, TechPortService, TechTransferService, TLEService, TrekWMSService
)
from app.core.config import get_settings
import asyncio

logger = logging.getLogger(__name__)
settings = get_settings()


# Helper to run async functions in tasks
def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


# ============================================================================
# APOD TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_apod(self):
    """Fetch latest APOD data."""
    try:
        service = APODService(settings.NASA_API_KEY)
        data = run_async(service.get_apod())
        
        if data:
            async def save_apod():
                async with async_session_maker() as session:
                    # Handle single item or list
                    items = data if isinstance(data, list) else [data]
                    
                    for item in items:
                        apod = APOD(
                            title=item.get('title'),
                            explanation=item.get('explanation'),
                            url=item.get('url'),
                            hdurl=item.get('hdurl'),
                            media_type=item.get('media_type', 'image'),
                            copyright=item.get('copyright'),
                            date=item.get('date'),
                            service_version=item.get('service_version'),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(apod)
                    
                    await session.commit()
            
            run_async(save_apod())
            logger.info(f"Successfully ingested APOD")
            return {"status": "success", "count": len(items) if isinstance(data, list) else 1}
        
        return {"status": "error", "message": "No data returned"}
    
    except Exception as exc:
        logger.error(f"Error ingesting APOD: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def ingest_apod_range(self, start_date: str, end_date: str):
    """Fetch APOD data for date range."""
    try:
        service = APODService(settings.NASA_API_KEY)
        data = run_async(service.get_apod_range(start_date, end_date))
        
        if data:
            async def save_apod_range():
                async with async_session_maker() as session:
                    items = data if isinstance(data, list) else [data]
                    
                    for item in items:
                        # Check if already exists
                        existing = await session.execute(
                            select(APOD).where(APOD.date == item.get('date'))
                        )
                        if not existing.scalar():
                            apod = APOD(
                                title=item.get('title'),
                                explanation=item.get('explanation'),
                                url=item.get('url'),
                                hdurl=item.get('hdurl'),
                                media_type=item.get('media_type', 'image'),
                                copyright=item.get('copyright'),
                                date=item.get('date'),
                                service_version=item.get('service_version'),
                                fetched_at=datetime.utcnow()
                            )
                            session.add(apod)
                    
                    await session.commit()
            
            run_async(save_apod_range())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting APOD range: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# ASTEROIDS TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_asteroids_today(self):
    """Fetch asteroids approaching today."""
    try:
        service = AsteroidsNeoWSService(settings.NASA_API_KEY)
        data = run_async(service.get_asteroids_today())
        
        if data and 'near_earth_objects' in data:
            async def save_asteroids():
                async with async_session_maker() as session:
                    for asteroids_list in data['near_earth_objects'].values():
                        for asteroid in asteroids_list:
                            neo_id = asteroid.get('id')
                            
                            # Check if already exists
                            existing = await session.execute(
                                select(AsteroidNeoWS).where(AsteroidNeoWS.neo_id == neo_id)
                            )
                            if existing.scalar():
                                continue
                            
                            # Extract close approach data
                            close_approaches = asteroid.get('close_approach_data', [])
                            if close_approaches:
                                approach = close_approaches[0]
                                
                                asteroid_record = AsteroidNeoWS(
                                    neo_id=neo_id,
                                    name=asteroid.get('name'),
                                    nasa_jpl_url=asteroid.get('nasa_jpl_url'),
                                    absolute_magnitude=asteroid.get('absolute_magnitude_h'),
                                    estimated_diameter_min_m=asteroid['estimated_diameter']['meters'].get('estimated_diameter_min'),
                                    estimated_diameter_max_m=asteroid['estimated_diameter']['meters'].get('estimated_diameter_max'),
                                    is_potentially_hazardous=asteroid.get('is_potentially_hazardous_asteroid', False),
                                    close_approach_date=datetime.fromisoformat(approach.get('close_approach_date_full', '').replace('Z', '+00:00')) if approach.get('close_approach_date_full') else None,
                                    close_approach_velocity_km_s=float(approach['relative_velocity'].get('kilometers_per_second', 0)),
                                    close_approach_distance_km=float(approach['miss_distance'].get('kilometers', 0)),
                                    relative_velocity=approach.get('relative_velocity'),
                                    miss_distance=approach.get('miss_distance'),
                                    orbiting_body=approach.get('orbiting_body'),
                                    fetched_at=datetime.utcnow()
                                )
                                session.add(asteroid_record)
                    
                    await session.commit()
            
            run_async(save_asteroids())
            logger.info(f"Successfully ingested asteroids")
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting asteroids: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def ingest_asteroids_by_date(self, start_date: str, end_date: str):
    """Fetch asteroids for date range."""
    try:
        service = AsteroidsNeoWSService(settings.NASA_API_KEY)
        data = run_async(service.get_asteroids_by_date(start_date, end_date))
        
        if data and 'near_earth_objects' in data:
            async def save_asteroids_range():
                async with async_session_maker() as session:
                    for asteroids_list in data['near_earth_objects'].values():
                        for asteroid in asteroids_list:
                            neo_id = asteroid.get('id')
                            existing = await session.execute(
                                select(AsteroidNeoWS).where(AsteroidNeoWS.neo_id == neo_id)
                            )
                            if existing.scalar():
                                continue
                            
                            close_approaches = asteroid.get('close_approach_data', [])
                            if close_approaches:
                                for approach in close_approaches:
                                    asteroid_record = AsteroidNeoWS(
                                        neo_id=neo_id,
                                        name=asteroid.get('name'),
                                        nasa_jpl_url=asteroid.get('nasa_jpl_url'),
                                        absolute_magnitude=asteroid.get('absolute_magnitude_h'),
                                        estimated_diameter_min_m=asteroid['estimated_diameter']['meters'].get('estimated_diameter_min'),
                                        estimated_diameter_max_m=asteroid['estimated_diameter']['meters'].get('estimated_diameter_max'),
                                        is_potentially_hazardous=asteroid.get('is_potentially_hazardous_asteroid', False),
                                        close_approach_date=datetime.fromisoformat(approach.get('close_approach_date_full', '').replace('Z', '+00:00')) if approach.get('close_approach_date_full') else None,
                                        close_approach_velocity_km_s=float(approach['relative_velocity'].get('kilometers_per_second', 0)),
                                        close_approach_distance_km=float(approach['miss_distance'].get('kilometers', 0)),
                                        relative_velocity=approach.get('relative_velocity'),
                                        miss_distance=approach.get('miss_distance'),
                                        orbiting_body=approach.get('orbiting_body'),
                                        fetched_at=datetime.utcnow()
                                    )
                                    session.add(asteroid_record)
                    
                    await session.commit()
            
            run_async(save_asteroids_range())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting asteroids by date: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# DONKI SPACE WEATHER TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_donki_flares(self):
    """Fetch solar flare events from DONKI."""
    try:
        service = DONKIService(settings.NASA_API_KEY)
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
        data = run_async(service.get_flare_events(start_date))
        
        if data:
            async def save_donki():
                async with async_session_maker() as session:
                    for event in data:
                        event_id = event.get('eventID')
                        existing = await session.execute(
                            select(DONKI).where(DONKI.event_id == event_id)
                        )
                        if existing.scalar():
                            continue
                        
                        donki = DONKI(
                            event_id=event_id,
                            event_type='FLR',
                            link_id=event.get('link'),
                            peak_time=datetime.fromisoformat(event.get('peakTime', '').replace('Z', '+00:00')) if event.get('peakTime') else None,
                            start_time=datetime.fromisoformat(event.get('beginTime', '').replace('Z', '+00:00')) if event.get('beginTime') else None,
                            end_time=datetime.fromisoformat(event.get('endTime', '').replace('Z', '+00:00')) if event.get('endTime') else None,
                            description=event.get('classType', ''),
                            linked_events=event.get('linkedEvents', []),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(donki)
                    
                    await session.commit()
            
            run_async(save_donki())
            logger.info(f"Successfully ingested DONKI solar flares")
            return {"status": "success", "count": len(data)}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting DONKI flares: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def ingest_donki_cme(self):
    """Fetch CME events from DONKI."""
    try:
        service = DONKIService(settings.NASA_API_KEY)
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
        data = run_async(service.get_cme_events(start_date))
        
        if data:
            async def save_cme():
                async with async_session_maker() as session:
                    for event in data:
                        event_id = event.get('eventID')
                        existing = await session.execute(
                            select(DONKI).where(DONKI.event_id == event_id)
                        )
                        if existing.scalar():
                            continue
                        
                        donki = DONKI(
                            event_id=event_id,
                            event_type='CME',
                            link_id=event.get('link'),
                            start_time=datetime.fromisoformat(event.get('startTime', '').replace('Z', '+00:00')) if event.get('startTime') else None,
                            description='Coronal Mass Ejection',
                            linked_events=event.get('linkedEvents', []),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(donki)
                    
                    await session.commit()
            
            run_async(save_cme())
            return {"status": "success", "count": len(data)}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting DONKI CME: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# EONET NATURAL EVENTS TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_eonet_events(self):
    """Fetch natural events from EONET."""
    try:
        service = EONETService(settings.NASA_API_KEY)
        data = run_async(service.get_events(limit=100))
        
        if data and 'events' in data:
            async def save_eonet():
                async with async_session_maker() as session:
                    for event in data['events']:
                        eonet_id = event.get('id')
                        existing = await session.execute(
                            select(EONET).where(EONET.eonet_id == eonet_id)
                        )
                        if existing.scalar():
                            continue
                        
                        eonet = EONET(
                            eonet_id=eonet_id,
                            event_type=event['categories'][0].get('title', 'Unknown') if event.get('categories') else 'Unknown',
                            event_title=event.get('title'),
                            description=event.get('description'),
                            closed=event.get('closed', False),
                            geometry=event.get('geometry', {}),
                            sources=event.get('sources', []),
                            categories=event.get('categories', []),
                            last_update=datetime.fromisoformat(event.get('updated', '').replace('Z', '+00:00')) if event.get('updated') else datetime.utcnow(),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(eonet)
                    
                    await session.commit()
            
            run_async(save_eonet())
            return {"status": "success", "count": len(data['events'])}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting EONET events: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# EPIC EARTH IMAGERY TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_epic_imagery(self):
    """Fetch latest Earth imagery from EPIC."""
    try:
        service = EPICService(settings.NASA_API_KEY)
        data = run_async(service.get_imagery())
        
        if data:
            async def save_epic():
                async with async_session_maker() as session:
                    items = data if isinstance(data, list) else [data]
                    
                    for item in items:
                        identifier = item.get('identifier')
                        existing = await session.execute(
                            select(EPIC).where(EPIC.identifier == identifier)
                        )
                        if existing.scalar():
                            continue
                        
                        epic = EPIC(
                            identifier=identifier,
                            caption=item.get('caption', ''),
                            image_name=item.get('image'),
                            centroid_coordinates=item.get('centroid_coordinates', {}),
                            dscovr_j2000_position=item.get('dscovr_j2000_position', {}),
                            lunar_j2000_position=item.get('lunar_j2000_position', {}),
                            sun_j2000_position=item.get('sun_j2000_position', {}),
                            attitude_quaternions=item.get('attitude_quaternions', {}),
                            instrument=item.get('instrument', 'EPIC'),
                            observation_date=datetime.fromisoformat(item.get('date', '').replace('Z', '+00:00')) if item.get('date') else datetime.utcnow(),
                            url=f"https://api.nasa.gov/EPIC/archive/natural/{item.get('date', '').split('T')[0].replace('-', '/')}/png/{item.get('image')}.png",
                            fetched_at=datetime.utcnow()
                        )
                        session.add(epic)
                    
                    await session.commit()
            
            run_async(save_epic())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting EPIC imagery: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# EXOPLANET ARCHIVE TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_habitable_exoplanets(self):
    """Fetch habitable exoplanets."""
    try:
        service = ExoplanetService(settings.NASA_API_KEY)
        data = run_async(service.get_habitable_exoplanets())
        
        if data and 'results' in data:
            async def save_exoplanets():
                async with async_session_maker() as session:
                    for planet in data['results']:
                        pl_name = planet.get('pl_name')
                        existing = await session.execute(
                            select(Exoplanet).where(Exoplanet.pl_name == pl_name)
                        )
                        if existing.scalar():
                            continue
                        
                        exoplanet = Exoplanet(
                            pl_name=pl_name,
                            hostname=planet.get('hostname'),
                            pl_type=planet.get('pl_type'),
                            pl_mass=planet.get('pl_mass'),
                            pl_radius=planet.get('pl_radius'),
                            pl_period=planet.get('pl_period'),
                            pl_semimajor_axis=planet.get('pl_semimajor_axis'),
                            pl_equilibrium_temp=planet.get('pl_equilibrium_temp'),
                            sy_distance=planet.get('sy_distance'),
                            st_teff=planet.get('st_teff'),
                            st_mass=planet.get('st_mass'),
                            st_radius=planet.get('st_radius'),
                            discovery_year=planet.get('pl_disc_year'),
                            discovery_method=planet.get('pl_discmethod'),
                            habitable_zone=True,
                            fetched_at=datetime.utcnow()
                        )
                        session.add(exoplanet)
                    
                    await session.commit()
            
            run_async(save_exoplanets())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting exoplanets: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# INSIGHT MARS WEATHER TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_insight_weather(self):
    """Fetch latest Mars weather data."""
    try:
        service = InSightWeatherService(settings.NASA_API_KEY)
        data = run_async(service.get_latest_weather())
        
        if data:
            async def save_insight():
                async with async_session_maker() as session:
                    for sol_key, sol_data in data.items():
                        if sol_key == 'disclaimer' or sol_key == 'validity_checks':
                            continue
                        
                        try:
                            sol = int(sol_key)
                        except ValueError:
                            continue
                        
                        existing = await session.execute(
                            select(InSightWeather).where(InSightWeather.sol == sol)
                        )
                        if existing.scalar():
                            continue
                        
                        weather = InSightWeather(
                            sol=sol,
                            season=sol_data.get('Season', ''),
                            ls=float(sol_data.get('LS', 0)),
                            min_temp_c=float(sol_data.get('Min Temp C', 0)) if sol_data.get('Min Temp C') else None,
                            max_temp_c=float(sol_data.get('Max Temp C', 0)) if sol_data.get('Max Temp C') else None,
                            avg_pressure=float(sol_data.get('Pressure', 0)) if sol_data.get('Pressure') else None,
                            wind_direction=sol_data.get('WD', {}),
                            wind_speed=sol_data.get('HWS', {}),
                            atmospheric_opacity=sol_data.get('AtmOpacity', {}),
                            sunrise=sol_data.get('Sunrise'),
                            sunset=sol_data.get('Sunset'),
                            earth_date=datetime.fromisoformat(sol_data.get('terrestrial_date', '').replace('Z', '+00:00')) if sol_data.get('terrestrial_date') else None,
                            fetched_at=datetime.utcnow()
                        )
                        session.add(weather)
                    
                    await session.commit()
            
            run_async(save_insight())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting InSight weather: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# NASA IMAGE LIBRARY TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_nasa_images(self, query: str = "space"):
    """Search and ingest NASA images."""
    try:
        service = NASAImageLibraryService(settings.NASA_API_KEY)
        data = run_async(service.search_images(query, limit=20))
        
        if data and 'collection' in data and 'items' in data['collection']:
            async def save_images():
                async with async_session_maker() as session:
                    for item in data['collection']['items']:
                        nasa_id = item['data'][0].get('nasa_id')
                        existing = await session.execute(
                            select(NASAImageLibrary).where(NASAImageLibrary.nasa_id == nasa_id)
                        )
                        if existing.scalar():
                            continue
                        
                        image = NASAImageLibrary(
                            nasa_id=nasa_id,
                            title=item['data'][0].get('title'),
                            description=item['data'][0].get('description', ''),
                            keywords=item['data'][0].get('keywords', []),
                            media_type='image',
                            location=item['data'][0].get('location'),
                            photographer=item['data'][0].get('photographer'),
                            date_created=datetime.fromisoformat(item['data'][0].get('date_created', '').replace('Z', '+00:00')) if item['data'][0].get('date_created') else None,
                            center=item['data'][0].get('center'),
                            album=item.get('href', ''),
                            links=[{'href': l.get('href'), 'rel': l.get('rel')} for l in item.get('links', [])],
                            preview_url=next((l['href'] for l in item.get('links', []) if l.get('rel') == 'preview'), ''),
                            data_last_updated=datetime.fromisoformat(item['data'][0].get('secondary_creator', '')),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(image)
                    
                    await session.commit()
            
            run_async(save_images())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting NASA images: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# SATELLITE TRACKING TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_tle_data(self):
    """Fetch satellite TLE data."""
    try:
        service = TLEService(settings.NASA_API_KEY)
        
        # Common satellites to track
        satellites = {
            '25544': 'ISS',  # International Space Station
            '39084': 'Hubble',  # Hubble Space Telescope
            '34602': 'GOES-18',  # Weather satellite
        }
        
        async def save_tle():
            async with async_session_maker() as session:
                for sat_id, sat_name in satellites.items():
                    data = run_async(service.get_tle_for_satellite(sat_id))
                    if data:
                        tle = TLE(
                            satellite_number=sat_id,
                            satellite_name=sat_name,
                            epoch=datetime.utcnow(),
                            tle_line0=sat_name,
                            tle_line1=data.get('tle_line1', ''),
                            tle_line2=data.get('tle_line2', ''),
                            inclination=0.0,  # Parse from TLE
                            raan=0.0,
                            eccentricity=0.0,
                            argument_perigee=0.0,
                            mean_anomaly=0.0,
                            mean_motion=0.0,
                            epoch_year=datetime.utcnow().year,
                            epoch_day=float(datetime.utcnow().timetuple().tm_yday),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(tle)
                
                await session.commit()
        
        run_async(save_tle())
        return {"status": "success"}
    
    except Exception as exc:
        logger.error(f"Error ingesting TLE data: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# CNEOS PLANETARY DEFENSE TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_cneos_data(self):
    """Fetch close approach data for planetary defense."""
    try:
        service = CNEOSService(settings.NASA_API_KEY)
        start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')
        end_date = (datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d')
        
        data = run_async(service.query_close_approaches(start_date, end_date))
        
        if data and 'data' in data:
            async def save_cneos():
                async with async_session_maker() as session:
                    for approach in data['data'][:100]:  # Limit to 100
                        designation = approach.get('des')
                        existing = await session.execute(
                            select(CNEOS).where(CNEOS.designation == designation)
                        )
                        if existing.scalar():
                            continue
                        
                        cneos = CNEOS(
                            designation=designation,
                            object_name=approach.get('name', ''),
                            object_type='asteroid',
                            epoch=datetime.utcnow(),
                            semi_major_axis=float(approach.get('a', 0)) if approach.get('a') else 0.0,
                            eccentricity=float(approach.get('e', 0)) if approach.get('e') else 0.0,
                            inclination=float(approach.get('i', 0)) if approach.get('i') else 0.0,
                            longitude_ascending_node=float(approach.get('om', 0)) if approach.get('om') else 0.0,
                            argument_perihelion=float(approach.get('w', 0)) if approach.get('w') else 0.0,
                            mean_anomaly=float(approach.get('ma', 0)) if approach.get('ma') else 0.0,
                            perihelion_distance=float(approach.get('q', 0)) if approach.get('q') else 0.0,
                            aphelion_distance=float(approach.get('ad', 0)) if approach.get('ad') else 0.0,
                            orbital_period=float(approach.get('per', 0)) if approach.get('per') else 0.0,
                            diameter_km=float(approach.get('diameter', 0)) if approach.get('diameter') else None,
                            absolute_magnitude=float(approach.get('H', 0)) if approach.get('H') else 0.0,
                            hazard_assessment='unknown',
                            fetched_at=datetime.utcnow()
                        )
                        session.add(cneos)
                    
                    await session.commit()
            
            run_async(save_cneos())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting CNEOS data: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# TECHPORT & TECHTRANSFER TASKS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def ingest_techport_projects(self):
    """Fetch NASA technology projects."""
    try:
        service = TechPortService(settings.NASA_API_KEY)
        data = run_async(service.get_projects())
        
        if data and 'projects' in data:
            async def save_projects():
                async with async_session_maker() as session:
                    for project in data['projects']:
                        project_id = str(project.get('projectId'))
                        existing = await session.execute(
                            select(TechPort).where(TechPort.project_id == project_id)
                        )
                        if existing.scalar():
                            continue
                        
                        tp = TechPort(
                            project_id=project_id,
                            title=project.get('title'),
                            description=project.get('description', ''),
                            status=project.get('statusDescription', 'Unknown'),
                            technology_maturity_level=int(project.get('trl', 1)) if project.get('trl') else 1,
                            start_date=datetime.fromisoformat(project.get('startDate', '').replace('Z', '+00:00')) if project.get('startDate') else None,
                            end_date=datetime.fromisoformat(project.get('endDate', '').replace('Z', '+00:00')) if project.get('endDate') else None,
                            organization=project.get('leadOrganization', ''),
                            program=project.get('program', {}).get('title', ''),
                            mission=project.get('mission', {}).get('title'),
                            benefits=project.get('benefits', []),
                            goals=project.get('goals', []),
                            url=project.get('url', ''),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(tp)
                    
                    await session.commit()
            
            run_async(save_projects())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting TechPort: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def ingest_techtransfer_spinoffs(self):
    """Fetch NASA spinoff technologies."""
    try:
        service = TechTransferService(settings.NASA_API_KEY)
        data = run_async(service.get_spinoffs())
        
        if data and 'spinoffs' in data:
            async def save_spinoffs():
                async with async_session_maker() as session:
                    for spinoff in data['spinoffs']:
                        spinoff_id = str(spinoff.get('id'))
                        existing = await session.execute(
                            select(TechTransfer).where(TechTransfer.spinoff_id == spinoff_id)
                        )
                        if existing.scalar():
                            continue
                        
                        tt = TechTransfer(
                            spinoff_id=spinoff_id,
                            title=spinoff.get('title'),
                            description=spinoff.get('description', ''),
                            benefits=spinoff.get('benefits', ''),
                            category=spinoff.get('category', ''),
                            year_first_published=int(spinoff.get('year_first_published', 2024)),
                            year_updated=int(spinoff.get('year_updated')) if spinoff.get('year_updated') else None,
                            agency=spinoff.get('agency', 'NASA'),
                            organization=spinoff.get('organization', ''),
                            application=spinoff.get('application', ''),
                            nasa_center=spinoff.get('nasa_center', ''),
                            status=spinoff.get('status', 'active'),
                            url=spinoff.get('url', ''),
                            fetched_at=datetime.utcnow()
                        )
                        session.add(tt)
                    
                    await session.commit()
            
            run_async(save_spinoffs())
            return {"status": "success"}
        
        return {"status": "error"}
    
    except Exception as exc:
        logger.error(f"Error ingesting TechTransfer: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


# ============================================================================
# SUMMARY INGESTION TASK
# ============================================================================

@shared_task(bind=True)
def ingest_all_nasa_data(self):
    """Master task to ingest all NASA data."""
    tasks = [
        ingest_apod.delay(),
        ingest_asteroids_today.delay(),
        ingest_donki_flares.delay(),
        ingest_donki_cme.delay(),
        ingest_eonet_events.delay(),
        ingest_epic_imagery.delay(),
        ingest_habitable_exoplanets.delay(),
        ingest_insight_weather.delay(),
        ingest_nasa_images.delay(query="space"),
        ingest_tle_data.delay(),
        ingest_cneos_data.delay(),
        ingest_techport_projects.delay(),
        ingest_techtransfer_spinoffs.delay(),
    ]
    
    return {
        "status": "queued",
        "task_count": len(tasks),
        "task_ids": [t.id for t in tasks]
    }
