from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db import get_db
from app.models import (
    SkyEventCreate, SkyEventResponse,
    SpaceWeatherAlertCreate, SpaceWeatherAlertResponse,
    MissionCreate, MissionResponse,
    PredictionCreate, PredictionResponse
)
from app.services import (
    SkyEventService, SpaceWeatherService, MissionService, PredictionService
)

router = APIRouter(prefix="/api/v1", tags=["Sky Events & Missions"])


# ============ SKY EVENTS ============
@router.post("/sky-events", response_model=SkyEventResponse)
async def create_sky_event(
    event: SkyEventCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new sky event (meteor shower, ISS pass, planetary alignment)."""
    event_data = event.model_dump()
    return await SkyEventService.create_sky_event(session, event_data)


@router.get("/sky-events/upcoming", response_model=List[SkyEventResponse])
async def get_upcoming_sky_events(
    days_ahead: int = 30,
    event_type: Optional[str] = None,
    session: AsyncSession = Depends(get_db)
):
    """Get upcoming sky events."""
    return await SkyEventService.get_upcoming_events(session, days_ahead, event_type)


@router.get("/sky-events/visible", response_model=List[SkyEventResponse])
async def get_visible_events(
    latitude: float,
    longitude: float,
    days_ahead: int = 30,
    session: AsyncSession = Depends(get_db)
):
    """Get sky events visible from a specific location."""
    return await SkyEventService.get_visible_events(
        session, latitude, longitude, days_ahead
    )


# ============ SPACE WEATHER ============
@router.post("/weather/alerts", response_model=SpaceWeatherAlertResponse)
async def create_weather_alert(
    alert: SpaceWeatherAlertCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create space weather alert."""
    alert_data = alert.model_dump()
    return await SpaceWeatherService.create_alert(session, alert_data)


@router.get("/weather/alerts/active", response_model=List[SpaceWeatherAlertResponse])
async def get_active_alerts(
    session: AsyncSession = Depends(get_db)
):
    """Get all active space weather alerts."""
    return await SpaceWeatherService.get_active_alerts(session)


@router.get("/weather/alerts/{alert_type}", response_model=List[SpaceWeatherAlertResponse])
async def get_alerts_by_type(
    alert_type: str,
    session: AsyncSession = Depends(get_db)
):
    """Get alerts by type (solar_flare, geomagnetic_storm, aurora, radiation)."""
    return await SpaceWeatherService.get_alerts_by_type(session, alert_type)


# ============ MISSIONS ============
@router.post("/missions", response_model=MissionResponse)
async def create_mission(
    mission: MissionCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new space mission."""
    mission_data = mission.model_dump()
    return await MissionService.create_mission(session, mission_data)


@router.get("/missions/status/{status}", response_model=List[MissionResponse])
async def get_missions_by_status(
    status: str,
    session: AsyncSession = Depends(get_db)
):
    """Get missions by status: past, active, or upcoming."""
    if status not in ["past", "active", "upcoming"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    return await MissionService.get_missions_by_status(session, status)


@router.get("/missions", response_model=List[MissionResponse])
async def get_all_missions(
    session: AsyncSession = Depends(get_db)
):
    """Get all missions."""
    return await MissionService.get_all_missions(session)


# ============ PREDICTIONS ============
@router.post("/predictions", response_model=PredictionResponse)
async def create_prediction(
    prediction: PredictionCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create AI prediction."""
    prediction_data = prediction.model_dump()
    return await PredictionService.create_prediction(session, prediction_data)


@router.get("/predictions/upcoming/{prediction_type}", response_model=List[PredictionResponse])
async def get_upcoming_predictions(
    prediction_type: str,
    days_ahead: int = 7,
    session: AsyncSession = Depends(get_db)
):
    """Get upcoming predictions by type."""
    return await PredictionService.get_upcoming_predictions(
        session, prediction_type, days_ahead
    )
