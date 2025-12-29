from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from typing import List, Optional
import logging
from app.models.db_models import (
    SkyEvent, SpaceWeatherAlert, Mission, Prediction,
    LearningContent, EarthImpactData
)

logger = logging.getLogger(__name__)


class SkyEventService:
    """Service for sky events (meteors, ISS, alignments)."""
    
    @staticmethod
    async def create_sky_event(session: AsyncSession, event_data: dict):
        """Create a new sky event."""
        try:
            event = SkyEvent(**event_data)
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event
        except Exception as e:
            logger.error(f"Error creating sky event: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_upcoming_events(
        session: AsyncSession,
        days_ahead: int = 30,
        event_type: Optional[str] = None
    ) -> List[SkyEvent]:
        """Get upcoming sky events."""
        try:
            now = datetime.utcnow()
            future = now + timedelta(days=days_ahead)
            
            query = select(SkyEvent).where(
                (SkyEvent.start_time >= now) &
                (SkyEvent.start_time <= future)
            )
            
            if event_type:
                query = query.where(SkyEvent.event_type == event_type)
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching upcoming events: {e}")
            return []
    
    @staticmethod
    async def get_visible_events(
        session: AsyncSession,
        latitude: float,
        longitude: float,
        days_ahead: int = 30
    ) -> List[SkyEvent]:
        """Get sky events visible from a location."""
        try:
            # TODO: Implement geographic filtering
            return await SkyEventService.get_upcoming_events(session, days_ahead)
        except Exception as e:
            logger.error(f"Error fetching visible events: {e}")
            return []


class SpaceWeatherService:
    """Service for space weather alerts."""
    
    @staticmethod
    async def create_alert(session: AsyncSession, alert_data: dict):
        """Create space weather alert."""
        try:
            alert = SpaceWeatherAlert(**alert_data)
            session.add(alert)
            await session.commit()
            await session.refresh(alert)
            return alert
        except Exception as e:
            logger.error(f"Error creating weather alert: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_active_alerts(session: AsyncSession) -> List[SpaceWeatherAlert]:
        """Get all active space weather alerts."""
        try:
            query = select(SpaceWeatherAlert).where(
                SpaceWeatherAlert.is_active == True
            ).order_by(SpaceWeatherAlert.severity.desc())
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching active alerts: {e}")
            return []
    
    @staticmethod
    async def get_alerts_by_type(
        session: AsyncSession,
        alert_type: str
    ) -> List[SpaceWeatherAlert]:
        """Get alerts by type."""
        try:
            query = select(SpaceWeatherAlert).where(
                SpaceWeatherAlert.alert_type == alert_type
            ).order_by(SpaceWeatherAlert.created_at.desc())
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching alerts by type: {e}")
            return []


class MissionService:
    """Service for space missions."""
    
    @staticmethod
    async def create_mission(session: AsyncSession, mission_data: dict):
        """Create a new mission."""
        try:
            mission = Mission(**mission_data)
            session.add(mission)
            await session.commit()
            await session.refresh(mission)
            return mission
        except Exception as e:
            logger.error(f"Error creating mission: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_missions_by_status(
        session: AsyncSession,
        status: str  # "past", "active", "upcoming"
    ) -> List[Mission]:
        """Get missions by status."""
        try:
            query = select(Mission).where(
                Mission.status == status
            ).order_by(Mission.launch_date.desc())
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching missions by status: {e}")
            return []
    
    @staticmethod
    async def get_all_missions(session: AsyncSession) -> List[Mission]:
        """Get all missions ordered by date."""
        try:
            query = select(Mission).order_by(Mission.launch_date.desc())
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching all missions: {e}")
            return []


class PredictionService:
    """Service for AI predictions."""
    
    @staticmethod
    async def create_prediction(session: AsyncSession, prediction_data: dict):
        """Create a prediction."""
        try:
            prediction = Prediction(**prediction_data)
            session.add(prediction)
            await session.commit()
            await session.refresh(prediction)
            return prediction
        except Exception as e:
            logger.error(f"Error creating prediction: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_upcoming_predictions(
        session: AsyncSession,
        prediction_type: str,
        days_ahead: int = 7
    ) -> List[Prediction]:
        """Get upcoming predictions."""
        try:
            now = datetime.utcnow()
            future = now + timedelta(days=days_ahead)
            
            query = select(Prediction).where(
                (Prediction.prediction_type == prediction_type) &
                (Prediction.target_date >= now) &
                (Prediction.target_date <= future) &
                (Prediction.is_verified == False)
            ).order_by(Prediction.target_date.asc())
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching upcoming predictions: {e}")
            return []


class LearningService:
    """Service for learning content."""
    
    @staticmethod
    async def create_content(session: AsyncSession, content_data: dict):
        """Create learning content."""
        try:
            content = LearningContent(**content_data)
            session.add(content)
            await session.commit()
            await session.refresh(content)
            return content
        except Exception as e:
            logger.error(f"Error creating learning content: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_published_content(
        session: AsyncSession,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[LearningContent]:
        """Get published learning content."""
        try:
            query = select(LearningContent).where(
                LearningContent.is_published == True
            )
            
            if category:
                query = query.where(LearningContent.category == category)
            if difficulty:
                query = query.where(LearningContent.difficulty_level == difficulty)
            
            query = query.order_by(LearningContent.view_count.desc())
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching published content: {e}")
            return []
    
    @staticmethod
    async def increment_view_count(session: AsyncSession, content_id: int):
        """Increment view count for content."""
        try:
            query = select(LearningContent).where(LearningContent.id == content_id)
            result = await session.execute(query)
            content = result.scalar_one_or_none()
            
            if content:
                content.view_count += 1
                await session.commit()
        except Exception as e:
            logger.error(f"Error incrementing view count: {e}")
            await session.rollback()


class EarthImpactService:
    """Service for Earth impact data."""
    
    @staticmethod
    async def create_impact_data(session: AsyncSession, data: dict):
        """Create Earth impact observation."""
        try:
            impact = EarthImpactData(**data)
            session.add(impact)
            await session.commit()
            await session.refresh(impact)
            return impact
        except Exception as e:
            logger.error(f"Error creating impact data: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_impact_by_type(
        session: AsyncSession,
        impact_type: str,
        limit: int = 50
    ) -> List[EarthImpactData]:
        """Get impact data by type."""
        try:
            query = select(EarthImpactData).where(
                EarthImpactData.impact_type == impact_type
            ).order_by(
                EarthImpactData.observation_date.desc()
            ).limit(limit)
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching impact by type: {e}")
            return []
    
    @staticmethod
    async def get_recent_impacts(
        session: AsyncSession,
        days: int = 7,
        limit: int = 100
    ) -> List[EarthImpactData]:
        """Get recent impact observations."""
        try:
            since = datetime.utcnow() - timedelta(days=days)
            
            query = select(EarthImpactData).where(
                EarthImpactData.observation_date >= since
            ).order_by(
                EarthImpactData.observation_date.desc()
            ).limit(limit)
            
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching recent impacts: {e}")
            return []
