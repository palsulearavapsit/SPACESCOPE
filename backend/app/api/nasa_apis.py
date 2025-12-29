"""
NASA APIs Routes - FastAPI endpoints for all 16 NASA APIs
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List, Optional
from app.db import get_db
from app.models.db_models import (
    APOD, AsteroidNeoWS, DONKI, EONET, EPIC, Exoplanet, GIBS,
    InSightWeather, NASAImageLibrary, OpenScience, SatelliteSituationCenter,
    CNEOS, TechPort, TechTransfer, TLE, TrekWMS
)
from app.models.schemas import (
    APODResponse, AsteroidNeoWSResponse, DONKIResponse, EONETResponse,
    EPICResponse, ExoplanetResponse, GIBSResponse, InSightWeatherResponse,
    NASAImageLibraryResponse, OpenScienceResponse, SatelliteSituationCenterResponse,
    CNEOSResponse, TechPortResponse, TechTransferResponse, TLEResponse, TrekWMSResponse,
    UnifiedSearchResponse
)
from app.tasks.nasa_ingestion import (
    ingest_apod, ingest_asteroids_today, ingest_donki_flares, ingest_eonet_events,
    ingest_epic_imagery, ingest_habitable_exoplanets, ingest_insight_weather,
    ingest_nasa_images, ingest_tle_data, ingest_cneos_data,
    ingest_techport_projects, ingest_techtransfer_spinoffs, ingest_all_nasa_data
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/nasa", tags=["NASA APIs"])


@router.get("/")
async def nasa_root():
    """Root summary for NASA API integrations."""
    return {
        "message": "NASA APIs",
        "endpoints": {
            "apod": "/api/v1/nasa/apod",
            "asteroids": "/api/v1/nasa/asteroids",
            "donki": "/api/v1/nasa/donki/space-weather",
            "search": "/api/v1/nasa/search",
            "health": "/api/v1/nasa/health"
        }
    }


# ============================================================================
# APOD ENDPOINTS
# ============================================================================

@router.get("/apod", response_model=List[APODResponse])
async def get_apod(db: AsyncSession = Depends(get_db), limit: int = Query(10)):
    """Get Astronomy Picture of the Day entries."""
    result = await db.execute(
        select(APOD).order_by(APOD.fetched_at.desc()).limit(limit)
    )
    return result.scalars().all()


@router.post("/apod/refresh")
async def refresh_apod():
    """Trigger APOD data ingestion."""
    task = ingest_apod.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# ASTEROIDS ENDPOINTS
# ============================================================================

@router.get("/asteroids", response_model=List[AsteroidNeoWSResponse])
async def get_asteroids(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20),
    hazardous_only: bool = Query(False)
):
    """Get asteroid data."""
    query = select(AsteroidNeoWS).order_by(AsteroidNeoWS.close_approach_date.desc())
    
    if hazardous_only:
        query = query.where(AsteroidNeoWS.is_potentially_hazardous == True)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/asteroids/{neo_id}", response_model=AsteroidNeoWSResponse)
async def get_asteroid(neo_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific asteroid."""
    result = await db.execute(
        select(AsteroidNeoWS).where(AsteroidNeoWS.neo_id == neo_id)
    )
    asteroid = result.scalar()
    if not asteroid:
        raise HTTPException(status_code=404, detail="Asteroid not found")
    return asteroid


@router.post("/asteroids/refresh")
async def refresh_asteroids():
    """Trigger asteroid data ingestion."""
    task = ingest_asteroids_today.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# DONKI SPACE WEATHER ENDPOINTS
# ============================================================================

@router.get("/donki/space-weather", response_model=List[DONKIResponse])
async def get_donki_events(
    db: AsyncSession = Depends(get_db),
    event_type: Optional[str] = Query(None),
    limit: int = Query(20)
):
    """Get DONKI space weather events."""
    query = select(DONKI).order_by(DONKI.start_time.desc())
    
    if event_type:
        query = query.where(DONKI.event_type == event_type)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/donki/flares", response_model=List[DONKIResponse])
async def get_solar_flares(db: AsyncSession = Depends(get_db), limit: int = Query(10)):
    """Get solar flare events."""
    result = await db.execute(
        select(DONKI).where(DONKI.event_type == 'FLR')
        .order_by(DONKI.peak_time.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.post("/donki/refresh")
async def refresh_donki():
    """Trigger DONKI data ingestion."""
    task1 = ingest_donki_flares.delay()
    task2 = ingest_donki_flares.delay()
    return {
        "status": "queued",
        "tasks": [{"type": "flares", "id": task1.id}, {"type": "cme", "id": task2.id}]
    }


# ============================================================================
# EONET NATURAL EVENTS ENDPOINTS
# ============================================================================

@router.get("/eonet/events", response_model=List[EONETResponse])
async def get_eonet_events(
    db: AsyncSession = Depends(get_db),
    event_type: Optional[str] = Query(None),
    limit: int = Query(20)
):
    """Get natural events."""
    query = select(EONET).order_by(EONET.last_update.desc())
    
    if event_type:
        query = query.where(EONET.event_type == event_type)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/eonet/refresh")
async def refresh_eonet():
    """Trigger EONET data ingestion."""
    task = ingest_eonet_events.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# EPIC EARTH IMAGERY ENDPOINTS
# ============================================================================

@router.get("/epic/imagery", response_model=List[EPICResponse])
async def get_epic_imagery(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20),
    recent: bool = Query(True)
):
    """Get Earth imagery from EPIC."""
    query = select(EPIC)
    
    if recent:
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        query = query.where(EPIC.observation_date >= cutoff_date)
    
    query = query.order_by(EPIC.observation_date.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/epic/refresh")
async def refresh_epic():
    """Trigger EPIC data ingestion."""
    task = ingest_epic_imagery.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# EXOPLANET ENDPOINTS
# ============================================================================

@router.get("/exoplanets", response_model=List[ExoplanetResponse])
async def get_exoplanets(
    db: AsyncSession = Depends(get_db),
    habitable_only: bool = Query(False),
    limit: int = Query(50)
):
    """Get exoplanet data."""
    query = select(Exoplanet)
    
    if habitable_only:
        query = query.where(Exoplanet.habitable_zone == True)
    
    query = query.order_by(Exoplanet.pl_equilibrium_temp.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/exoplanets/{pl_name}", response_model=ExoplanetResponse)
async def get_exoplanet(pl_name: str, db: AsyncSession = Depends(get_db)):
    """Get specific exoplanet."""
    result = await db.execute(
        select(Exoplanet).where(Exoplanet.pl_name == pl_name)
    )
    planet = result.scalar()
    if not planet:
        raise HTTPException(status_code=404, detail="Exoplanet not found")
    return planet


@router.post("/exoplanets/refresh")
async def refresh_exoplanets():
    """Trigger exoplanet data ingestion."""
    task = ingest_habitable_exoplanets.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# INSIGHT MARS WEATHER ENDPOINTS
# ============================================================================

@router.get("/mars-weather", response_model=List[InSightWeatherResponse])
async def get_mars_weather(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(30)
):
    """Get Mars weather data."""
    result = await db.execute(
        select(InSightWeather).order_by(InSightWeather.sol.desc()).limit(limit)
    )
    return result.scalars().all()


@router.get("/mars-weather/{sol}", response_model=InSightWeatherResponse)
async def get_mars_weather_by_sol(sol: int, db: AsyncSession = Depends(get_db)):
    """Get Mars weather for specific sol."""
    result = await db.execute(
        select(InSightWeather).where(InSightWeather.sol == sol)
    )
    weather = result.scalar()
    if not weather:
        raise HTTPException(status_code=404, detail="Sol weather data not found")
    return weather


@router.post("/mars-weather/refresh")
async def refresh_mars_weather():
    """Trigger Mars weather data ingestion."""
    task = ingest_insight_weather.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# NASA IMAGE LIBRARY ENDPOINTS
# ============================================================================

@router.get("/images", response_model=List[NASAImageLibraryResponse])
async def get_nasa_images(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20)
):
    """Get NASA images and videos."""
    result = await db.execute(
        select(NASAImageLibrary).order_by(NASAImageLibrary.date_created.desc()).limit(limit)
    )
    return result.scalars().all()


@router.get("/images/search/{query_str}", response_model=List[NASAImageLibraryResponse])
async def search_nasa_images(query_str: str):
    """Search NASA images - triggers new ingestion."""
    task = ingest_nasa_images.delay(query=query_str)
    return {"task_id": task.id, "status": "queued", "search_query": query_str}


# ============================================================================
# SATELLITE TRACKING ENDPOINTS
# ============================================================================

@router.get("/satellites", response_model=List[SatelliteSituationCenterResponse])
async def get_satellites(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50)
):
    """Get active satellites."""
    result = await db.execute(
        select(SatelliteSituationCenter).limit(limit)
    )
    return result.scalars().all()


@router.get("/tle", response_model=List[TLEResponse])
async def get_tle_data(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20)
):
    """Get TLE (Two-Line Element) data for satellites."""
    result = await db.execute(
        select(TLE).order_by(TLE.fetched_at.desc()).limit(limit)
    )
    return result.scalars().all()


@router.post("/tle/refresh")
async def refresh_tle():
    """Trigger TLE data ingestion."""
    task = ingest_tle_data.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# CNEOS PLANETARY DEFENSE ENDPOINTS
# ============================================================================

@router.get("/cneos/close-approaches", response_model=List[CNEOSResponse])
async def get_close_approaches(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50),
    hazard_only: bool = Query(False)
):
    """Get near-Earth object close approaches."""
    query = select(CNEOS).order_by(CNEOS.epoch.desc())
    
    if hazard_only:
        query = query.where(CNEOS.hazard_assessment != 'safe')
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/cneos/{designation}", response_model=CNEOSResponse)
async def get_cneos_object(designation: str, db: AsyncSession = Depends(get_db)):
    """Get specific near-Earth object."""
    result = await db.execute(
        select(CNEOS).where(CNEOS.designation == designation)
    )
    obj = result.scalar()
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj


@router.post("/cneos/refresh")
async def refresh_cneos():
    """Trigger CNEOS data ingestion."""
    task = ingest_cneos_data.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# TECHPORT ENDPOINTS
# ============================================================================

@router.get("/techport/projects", response_model=List[TechPortResponse])
async def get_tech_projects(
    db: AsyncSession = Depends(get_db),
    status: Optional[str] = Query(None),
    limit: int = Query(50)
):
    """Get NASA technology projects."""
    query = select(TechPort)
    
    if status:
        query = query.where(TechPort.status == status)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/techport/projects/{project_id}", response_model=TechPortResponse)
async def get_tech_project(project_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific technology project."""
    result = await db.execute(
        select(TechPort).where(TechPort.project_id == project_id)
    )
    project = result.scalar()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/techport/refresh")
async def refresh_techport():
    """Trigger TechPort data ingestion."""
    task = ingest_techport_projects.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# TECHTRANSFER ENDPOINTS
# ============================================================================

@router.get("/techtransfer/spinoffs", response_model=List[TechTransferResponse])
async def get_spinoffs(
    db: AsyncSession = Depends(get_db),
    category: Optional[str] = Query(None),
    limit: int = Query(50)
):
    """Get NASA spinoff technologies."""
    query = select(TechTransfer)
    
    if category:
        query = query.where(TechTransfer.category == category)
    
    query = query.order_by(TechTransfer.year_first_published.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/techtransfer/spinoffs/{spinoff_id}", response_model=TechTransferResponse)
async def get_spinoff(spinoff_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific spinoff technology."""
    result = await db.execute(
        select(TechTransfer).where(TechTransfer.spinoff_id == spinoff_id)
    )
    spinoff = result.scalar()
    if not spinoff:
        raise HTTPException(status_code=404, detail="Spinoff not found")
    return spinoff


@router.post("/techtransfer/refresh")
async def refresh_techtransfer():
    """Trigger TechTransfer data ingestion."""
    task = ingest_techtransfer_spinoffs.delay()
    return {"task_id": task.id, "status": "queued"}


# ============================================================================
# UNIFIED SEARCH ENDPOINT
# ============================================================================

@router.get("/search", response_model=List[UnifiedSearchResponse])
async def unified_search(
    q: str = Query(..., description="Search query"),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20)
):
    """
    Unified search across all NASA APIs.
    Searches titles, descriptions, keywords across all datasets.
    """
    results = []
    
    # Search APOD
    apod_results = await db.execute(
        select(APOD).where(
            (APOD.title.ilike(f"%{q}%")) |
            (APOD.explanation.ilike(f"%{q}%"))
        ).limit(limit)
    )
    for item in apod_results.scalars():
        results.append({
            "result_type": "apod",
            "result_id": item.id,
            "title": item.title,
            "description": item.explanation,
            "relevance_score": 0.95,
            "data": {
                "url": item.url,
                "date": item.date,
                "media_type": item.media_type
            }
        })
    
    # Search Asteroids
    asteroid_results = await db.execute(
        select(AsteroidNeoWS).where(
            AsteroidNeoWS.name.ilike(f"%{q}%")
        ).limit(limit)
    )
    for item in asteroid_results.scalars():
        results.append({
            "result_type": "asteroid",
            "result_id": item.id,
            "title": item.name,
            "description": f"NEO ID: {item.neo_id}",
            "relevance_score": 0.90,
            "data": {
                "neo_id": item.neo_id,
                "hazardous": item.is_potentially_hazardous,
                "diameter_m": {
                    "min": item.estimated_diameter_min_m,
                    "max": item.estimated_diameter_max_m
                }
            }
        })
    
    # Search Exoplanets
    exoplanet_results = await db.execute(
        select(Exoplanet).where(
            (Exoplanet.pl_name.ilike(f"%{q}%")) |
            (Exoplanet.hostname.ilike(f"%{q}%"))
        ).limit(limit)
    )
    for item in exoplanet_results.scalars():
        results.append({
            "result_type": "exoplanet",
            "result_id": item.id,
            "title": item.pl_name,
            "description": f"Orbiting {item.hostname}",
            "relevance_score": 0.85,
            "data": {
                "host_star": item.hostname,
                "habitable_zone": item.habitable_zone,
                "mass_earth_masses": item.pl_mass
            }
        })
    
    # Search NASA Images
    image_results = await db.execute(
        select(NASAImageLibrary).where(
            (NASAImageLibrary.title.ilike(f"%{q}%")) |
            (NASAImageLibrary.description.ilike(f"%{q}%"))
        ).limit(limit)
    )
    for item in image_results.scalars():
        results.append({
            "result_type": "image",
            "result_id": item.id,
            "title": item.title,
            "description": item.description,
            "relevance_score": 0.80,
            "data": {
                "nasa_id": item.nasa_id,
                "media_type": item.media_type,
                "preview_url": item.preview_url
            }
        })
    
    # Sort by relevance and limit
    results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)[:limit]
    return results


# ============================================================================
# MASTER INGESTION ENDPOINT
# ============================================================================

@router.post("/ingest-all")
async def ingest_all_data():
    """Trigger ingestion of all NASA data."""
    task = ingest_all_nasa_data.delay()
    return {
        "status": "queued",
        "master_task_id": task.id,
        "message": "All NASA API data ingestion started"
    }


# ============================================================================
# STATS AND STATUS ENDPOINTS
# ============================================================================

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get statistics on ingested data."""
    stats = {}
    
    # Count records in each table
    for model, name in [
        (APOD, "apod"),
        (AsteroidNeoWS, "asteroids"),
        (DONKI, "donki"),
        (EONET, "eonet"),
        (EPIC, "epic"),
        (Exoplanet, "exoplanets"),
        (InSightWeather, "mars_weather"),
        (NASAImageLibrary, "images"),
        (SatelliteSituationCenter, "satellites"),
        (TLE, "tle"),
        (CNEOS, "cneos"),
        (TechPort, "techport"),
        (TechTransfer, "techtransfer"),
    ]:
        count = await db.scalar(select(model.__table__.func.count()).select_from(model))
        stats[name] = count or 0
    
    return {
        "total_records": sum(stats.values()),
        "breakdown": stats,
        "timestamp": datetime.utcnow()
    }


@router.get("/health")
async def nasa_apis_health(db: AsyncSession = Depends(get_db)):
    """Health check for all NASA API integrations."""
    health = {}
    
    # Check each API
    for model, name in [
        (APOD, "apod"),
        (AsteroidNeoWS, "asteroids"),
        (DONKI, "donki"),
        (EONET, "eonet"),
        (EPIC, "epic"),
        (Exoplanet, "exoplanets"),
        (InSightWeather, "mars_weather"),
        (NASAImageLibrary, "images"),
        (SatelliteSituationCenter, "satellites"),
        (TLE, "tle"),
        (CNEOS, "cneos"),
        (TechPort, "techport"),
        (TechTransfer, "techtransfer"),
    ]:
        try:
            result = await db.execute(select(model).limit(1))
            has_data = result.scalar() is not None
            health[name] = {
                "status": "healthy" if has_data else "no_data",
                "has_records": has_data
            }
        except Exception as e:
            health[name] = {
                "status": "error",
                "error": str(e)
            }
    
    overall = "healthy" if all(h["status"] == "healthy" for h in health.values()) else "degraded"
    
    return {
        "status": overall,
        "apis": health,
        "timestamp": datetime.utcnow()
    }
