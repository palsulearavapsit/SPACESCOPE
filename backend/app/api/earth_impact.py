from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import get_db
from app.models import EarthImpactDataCreate, EarthImpactDataResponse
from app.services import EarthImpactService

router = APIRouter(prefix="/api/v1", tags=["Earth Impact"])


@router.post("/earth-impact", response_model=EarthImpactDataResponse)
async def create_impact_data(
    data: EarthImpactDataCreate,
    session: AsyncSession = Depends(get_db)
):
    """Record satellite data impact on Earth (climate, disasters, pollution, agriculture)."""
    impact_data = data.model_dump()
    return await EarthImpactService.create_impact_data(session, impact_data)


@router.get("/earth-impact/{impact_type}", response_model=List[EarthImpactDataResponse])
async def get_impact_by_type(
    impact_type: str,
    limit: int = 50,
    session: AsyncSession = Depends(get_db)
):
    """Get Earth impact data by type: climate, disaster, pollution, agriculture."""
    return await EarthImpactService.get_impact_by_type(session, impact_type, limit)


@router.get("/earth-impact/recent", response_model=List[EarthImpactDataResponse])
async def get_recent_impacts(
    days: int = 7,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    """Get recent Earth impact observations."""
    return await EarthImpactService.get_recent_impacts(session, days, limit)
