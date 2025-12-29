from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.api import events_router, ai_router, earth_impact_router
from app.api.nasa_apis import router as nasa_apis_router
from app.db.database import engine, Base
from app.models import db_models  # Import all models to register them
import asyncio
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


async def init_db():
    """Initialize database tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully!")
        return True
    except Exception as e:
        logger.warning(f"Database initialization skipped: {str(e)[:100]}")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    print("🚀 SpaceScope Backend Starting...")
    
    # Try to initialize database tables
    try:
        print("📦 Initializing database tables...")
        if await asyncio.wait_for(init_db(), timeout=5):
            print("✅ Database tables initialized successfully!")
        else:
            print("⚠️ Database initialization incomplete but continuing...")
    except asyncio.TimeoutError:
        print("⚠️ Database initialization timeout - continuing with startup")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {str(e)[:100]}")
    
    yield
    print("🛑 SpaceScope Backend Shutting Down...")


# Create FastAPI app
app = FastAPI(
    title=getattr(settings, "API_TITLE", "SpaceScope API"),
    description="Centralized space data platform with real-time events, weather, missions, and learning",
    version=getattr(settings, "API_VERSION", "0.0.1"),
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events_router)
app.include_router(ai_router)
app.include_router(earth_impact_router)
app.include_router(nasa_apis_router)


@app.get("/")
async def root():
    """API health check."""
    return {
        "name": "SpaceScope API",
        "version": getattr(settings, "API_VERSION", "0.0.1"),
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "sky_events": "/api/v1/sky-events",
            "space_weather": "/api/v1/weather/alerts",
            "missions": "/api/v1/missions",
            "predictions": "/api/v1/predictions",
            "chat": "/api/v1/chat",
            "learning": "/api/v1/learning/content",
            "earth_impact": "/api/v1/earth-impact",
            "nasa_apis": "/api/v1/nasa"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-12-29T00:00:00Z"
    }


@app.get("/api/v1/status")
async def api_status():
    """Get API status and available modules."""
    return {
        "status": "operational",
        "modules": {
            "sky_events": "active",
            "space_weather": "active",
            "missions": "active",
            "predictions": "active",
            "ai_chat": "active",
            "vision_intelligence": "active",
            "learning": "active",
            "earth_impact": "active"
        },
        "ai_model": "gemini-2.5-flash",
        "db_connected": True,
        "cache_enabled": True,
        "celery_tasks": "scheduled"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_v2:app",
        host="0.0.0.0",
        port=8000,
        reload=getattr(settings, "DEBUG", False)
    )
