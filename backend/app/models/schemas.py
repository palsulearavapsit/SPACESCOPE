from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
import json


# ============ SKY EVENTS ============
class SkyEventBase(BaseModel):
    event_type: str
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    peak_time: Optional[datetime] = None
    visibility_zones: List[dict]
    magnitude: Optional[float] = None
    is_visible_worldwide: bool = False


class SkyEventCreate(SkyEventBase):
    pass


class SkyEventResponse(SkyEventBase):
    id: int
    visibility_percentage: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ SPACE WEATHER ============
class SpaceWeatherAlertBase(BaseModel):
    alert_type: str
    severity: str
    title: str
    description: str
    detected_at: datetime
    estimated_impact_time: Optional[datetime] = None
    affected_regions: List[dict]
    impact_summary: Optional[str] = None


class SpaceWeatherAlertCreate(SpaceWeatherAlertBase):
    pass


class SpaceWeatherAlertResponse(SpaceWeatherAlertBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ MISSIONS ============
class MissionBase(BaseModel):
    name: str
    mission_type: str
    status: str
    organization: str
    launch_date: datetime
    landing_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: str
    objectives: List[str]


class MissionCreate(MissionBase):
    achievements: Optional[List[str]] = None
    mission_timeline: Optional[dict] = None
    image_url: Optional[str] = None


class MissionResponse(MissionBase):
    id: int
    achievements: Optional[List[str]]
    mission_timeline: Optional[dict]
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ PREDICTIONS ============
class PredictionBase(BaseModel):
    prediction_type: str
    target_date: datetime
    probability: float
    confidence_score: float
    predicted_values: dict
    model_version: str


class PredictionCreate(PredictionBase):
    pass


class PredictionResponse(PredictionBase):
    id: int
    is_verified: bool
    actual_values: Optional[dict]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ LEARNING CONTENT ============
class LearningContentBase(BaseModel):
    title: str
    content_type: str
    category: str
    description: str
    difficulty_level: str
    estimated_time_minutes: int


class LearningContentCreate(LearningContentBase):
    content: str
    quiz_questions: Optional[List[dict]] = None
    is_published: bool = False


class LearningContentResponse(LearningContentBase):
    id: int
    content: str
    quiz_questions: Optional[List[dict]]
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QuizSubmission(BaseModel):
    content_id: int
    answers: List[int]  # Answer indices


# ============ EARTH IMPACT ============
class EarthImpactDataBase(BaseModel):
    impact_type: str
    location: str
    latitude: float
    longitude: float
    satellite_source: str
    metric_name: str
    metric_value: float
    unit: str
    observation_date: datetime
    insight: str


class EarthImpactDataCreate(EarthImpactDataBase):
    image_url: Optional[str] = None


class EarthImpactDataResponse(EarthImpactDataBase):
    id: int
    image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ USER & AUTH ============
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ============ CHAT & AI ============
class ChatMessage(BaseModel):
    user_message: str
    context_type: Optional[str] = None


class ChatResponse(BaseModel):
    ai_response: str
    context_data: Optional[dict] = None
    tokens_used: Optional[int] = None


# ============ ALERTS ============
class AlertResponse(BaseModel):
    id: int
    alert_type: str
    title: str
    message: str
    is_read: bool
    is_urgent: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# NASA API SCHEMAS (16 APIs)
# ============================================================================

# ============ APOD (Astronomy Picture of the Day) ============
class APODResponse(BaseModel):
    id: int
    title: str
    explanation: str
    url: str
    hdurl: Optional[str] = None
    media_type: str
    copyright: Optional[str] = None
    date: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ Asteroids NeoWs ============
class AsteroidNeoWSResponse(BaseModel):
    id: int
    neo_id: str
    name: str
    nasa_jpl_url: str
    absolute_magnitude: float
    estimated_diameter_min_m: float
    estimated_diameter_max_m: float
    is_potentially_hazardous: bool
    close_approach_date: Optional[datetime] = None
    close_approach_velocity_km_s: Optional[float] = None
    close_approach_distance_km: Optional[float] = None
    relative_velocity: Optional[dict] = None
    miss_distance: Optional[dict] = None
    orbiting_body: Optional[str] = None
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ DONKI (Space Weather) ============
class DONKIResponse(BaseModel):
    id: int
    event_id: str
    event_type: str
    link_id: str
    activity_id: Optional[str] = None
    peak_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    description: str
    linked_events: Optional[List[dict]] = None
    source_location: Optional[dict] = None
    active_region_number: Optional[int] = None
    synoptic_sequence: Optional[int] = None
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ EONET (Natural Events) ============
class EONETResponse(BaseModel):
    id: int
    eonet_id: str
    event_type: str
    event_title: str
    description: Optional[str] = None
    closed: bool
    geometry: dict
    sources: List[dict]
    categories: List[dict]
    last_update: datetime
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ EPIC (Earth Imagery) ============
class EPICResponse(BaseModel):
    id: int
    identifier: str
    caption: str
    image_name: str
    centroid_coordinates: dict
    dscovr_j2000_position: dict
    lunar_j2000_position: dict
    sun_j2000_position: dict
    attitude_quaternions: dict
    instrument: str
    observation_date: datetime
    url: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ Exoplanet Archive ============
class ExoplanetResponse(BaseModel):
    id: int
    pl_name: str
    hostname: str
    pl_type: Optional[str] = None
    pl_mass: Optional[float] = None
    pl_radius: Optional[float] = None
    pl_period: Optional[float] = None
    pl_semimajor_axis: Optional[float] = None
    pl_equilibrium_temp: Optional[float] = None
    sy_distance: Optional[float] = None
    st_teff: Optional[float] = None
    st_mass: Optional[float] = None
    st_radius: Optional[float] = None
    discovery_year: Optional[int] = None
    discovery_method: Optional[str] = None
    habitable_zone: bool
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ GIBS (Global Imagery) ============
class GIBSResponse(BaseModel):
    id: int
    layer_name: str
    product_type: str
    description: Optional[str] = None
    projection: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: str
    tile_coordinates: dict
    image_metadata: dict
    resolution: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ InSight Mars Weather ============
class InSightWeatherResponse(BaseModel):
    id: int
    sol: int
    season: str
    ls: float
    min_temp_c: Optional[float] = None
    max_temp_c: Optional[float] = None
    avg_pressure: Optional[float] = None
    wind_direction: Optional[dict] = None
    wind_speed: Optional[dict] = None
    atmospheric_opacity: Optional[dict] = None
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    earth_date: datetime
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ NASA Image & Video Library ============
class NASAImageLibraryResponse(BaseModel):
    id: int
    nasa_id: str
    title: str
    description: str
    keywords: List[str]
    media_type: str
    location: Optional[str] = None
    photographer: Optional[str] = None
    date_created: datetime
    center: str
    album: dict
    links: dict
    preview_url: str
    data_last_updated: datetime
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ Open Science Data Repository ============
class OpenScienceResponse(BaseModel):
    id: int
    dataset_id: str
    title: str
    description: str
    discipline: str
    doi: Optional[str] = None
    authors: List[str]
    publication_date: datetime
    keywords: List[str]
    file_count: int
    file_size_bytes: int
    format_types: List[str]
    access_level: str
    source_repository: str
    url: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ Satellite Situation Center ============
class SatelliteSituationCenterResponse(BaseModel):
    id: int
    satellite_id: str
    satellite_name: str
    sat_number: str
    mission_name: str
    organization: str
    country_of_registry: str
    launch_date: datetime
    launch_site: str
    orbital_period_minutes: Optional[float] = None
    orbital_inclination: Optional[float] = None
    apogee_km: Optional[float] = None
    perigee_km: Optional[float] = None
    operational_status: str
    primary_mission: str
    position: Optional[dict] = None
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ CNEOS (Planetary Defense) ============
class CNEOSResponse(BaseModel):
    id: int
    designation: str
    object_name: str
    object_type: str
    epoch: datetime
    semi_major_axis: float
    eccentricity: float
    inclination: float
    longitude_ascending_node: float
    argument_perihelion: float
    mean_anomaly: float
    perihelion_distance: float
    aphelion_distance: float
    orbital_period: float
    diameter_km: Optional[float] = None
    absolute_magnitude: float
    hazard_assessment: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ TechPort ============
class TechPortResponse(BaseModel):
    id: int
    project_id: str
    title: str
    description: str
    status: str
    technology_maturity_level: int
    start_date: datetime
    end_date: Optional[datetime] = None
    organization: str
    program: str
    mission: Optional[str] = None
    benefits: List[str]
    goals: List[str]
    url: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ TechTransfer ============
class TechTransferResponse(BaseModel):
    id: int
    spinoff_id: str
    title: str
    description: str
    benefits: str
    category: str
    year_first_published: int
    year_updated: Optional[int] = None
    agency: str
    organization: str
    application: str
    nasa_center: str
    status: str
    url: str
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ TLE (Satellite Tracking) ============
class TLEResponse(BaseModel):
    id: int
    satellite_number: str
    satellite_name: str
    epoch: datetime
    tle_line0: str
    tle_line1: str
    tle_line2: str
    inclination: float
    raan: float
    eccentricity: float
    argument_perigee: float
    mean_anomaly: float
    mean_motion: float
    epoch_year: int
    epoch_day: float
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ Trek WMS (Planetary Imagery) ============
class TrekWMSResponse(BaseModel):
    id: int
    body: str
    product_name: str
    layer_identifier: str
    description: Optional[str] = None
    style: str
    crs: str
    bbox: dict
    image_url: str
    transparent: bool
    opaque: bool
    queryable: bool
    metadata_url: Optional[str] = None
    fetched_at: datetime
    
    class Config:
        from_attributes = True


# ============ UNIFIED SEARCH ============
class UnifiedSearchResponse(BaseModel):
    result_type: str  # "apod", "asteroid", "mission", "exoplanet", etc.
    result_id: int
    title: str
    description: Optional[str] = None
    relevance_score: float
    data: dict  # Full result data
