"""Database initialization and migration script."""

import asyncio
from app.db.database import engine, Base
from app.models.db_models import (
    User, SkyEvent, SpaceWeatherAlert, Mission,
    Prediction, Alert, LearningContent, LearningProgress,
    EarthImpactData, ChatHistory, APOD, AsteroidNeoWS,
    DONKI, EONET, EPIC, Exoplanet, GIBS, InSightWeather,
    NASAImageLibrary, OpenScience, SatelliteSituationCenter,
    CNEOS, TechPort, TechTransfer, TLE, TrekWMS
)


async def init_db():
    """Initialize database and create tables."""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
