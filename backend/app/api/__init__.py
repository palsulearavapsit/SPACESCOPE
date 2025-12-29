from .events import router as events_router
from .ai import router as ai_router
from .earth_impact import router as earth_impact_router

__all__ = ["events_router", "ai_router", "earth_impact_router"]
