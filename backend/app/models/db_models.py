from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db import Base


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alerts = relationship("Alert", back_populates="user")
    learning_progress = relationship("LearningProgress", back_populates="user")


class SkyEvent(Base):
    """Sky event model (meteor showers, ISS passes, planetary alignments)."""
    __tablename__ = "sky_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)  # "meteor_shower", "iss_pass", "planetary_alignment"
    name = Column(String)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    peak_time = Column(DateTime, nullable=True)
    visibility_zones = Column(JSON)  # List of lat/lon coordinates
    magnitude = Column(Float, nullable=True)  # For meteor showers
    is_visible_worldwide = Column(Boolean, default=False)
    visibility_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SpaceWeatherAlert(Base):
    """Real-time space weather alerts."""
    __tablename__ = "space_weather_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String, index=True)  # "solar_flare", "geomagnetic_storm", "aurora", "radiation"
    severity = Column(String)  # "low", "moderate", "high", "extreme"
    title = Column(String)
    description = Column(Text)
    detected_at = Column(DateTime)
    estimated_impact_time = Column(DateTime, nullable=True)
    affected_regions = Column(JSON)  # List of lat/lon boxes
    impact_summary = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Mission(Base):
    """Space missions (past, present, future)."""
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    mission_type = Column(String)  # "satellite", "rover", "crewed", "probe"
    status = Column(String)  # "past", "active", "upcoming"
    organization = Column(String)
    launch_date = Column(DateTime)
    landing_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    description = Column(Text)
    objectives = Column(JSON)  # List of objectives
    achievements = Column(JSON, nullable=True)  # List of achievements
    mission_timeline = Column(JSON)  # Milestones with dates
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Prediction(Base):
    """AI predictions for space events."""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_type = Column(String, index=True)  # "solar_storm", "geomagnetic", "iss_pass", "aurora"
    target_date = Column(DateTime)
    probability = Column(Float)  # 0.0 to 1.0
    confidence_score = Column(Float)  # Model confidence
    predicted_values = Column(JSON)  # Model output details
    actual_values = Column(JSON, nullable=True)  # Ground truth after event
    is_verified = Column(Boolean, default=False)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Alert(Base):
    """User-specific alerts and notifications."""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String)  # "sky_event", "weather", "mission", "learning"
    title = Column(String)
    message = Column(Text)
    related_event_id = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="alerts")


class LearningContent(Base):
    """Educational content (quizzes, infographics, explanations)."""
    __tablename__ = "learning_content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content_type = Column(String)  # "quiz", "infographic", "article", "video"
    category = Column(String)  # "astronomy", "space_weather", "missions", "earth_observation"
    description = Column(Text)
    content = Column(Text)  # HTML or markdown
    difficulty_level = Column(String)  # "beginner", "intermediate", "advanced"
    estimated_time_minutes = Column(Integer)
    quiz_questions = Column(JSON, nullable=True)  # For quiz type
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearningProgress(Base):
    """User progress in learning."""
    __tablename__ = "learning_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("learning_content.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    quiz_score = Column(Float, nullable=True)
    is_completed = Column(Boolean, default=False)
    time_spent_minutes = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="learning_progress")


class EarthImpactData(Base):
    """Satellite data impact on Earth (climate, disasters, pollution, agriculture)."""
    __tablename__ = "earth_impact_data"
    
    id = Column(Integer, primary_key=True, index=True)
    impact_type = Column(String)  # "climate", "disaster", "pollution", "agriculture"
    location = Column(String)  # Region name
    latitude = Column(Float)
    longitude = Column(Float)
    satellite_source = Column(String)  # Which satellite provided data
    metric_name = Column(String)
    metric_value = Column(Float)
    unit = Column(String)
    observation_date = Column(DateTime)
    insight = Column(Text)  # AI-generated insight
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatHistory(Base):
    """Conversational AI chat history."""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_message = Column(Text)
    ai_response = Column(Text)
    context_type = Column(String)  # "events", "weather", "missions", "learning"
    context_data = Column(JSON, nullable=True)
    model_used = Column(String)  # "gemini-2.5-flash"
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# NASA API INTEGRATION MODELS (16 APIs)
# ============================================================================

class APOD(Base):
    """Astronomy Picture of the Day"""
    __tablename__ = "apod"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    explanation = Column(Text)
    url = Column(String, unique=True)
    hdurl = Column(String, nullable=True)
    media_type = Column(String)  # "image" or "video"
    copyright = Column(String, nullable=True)
    date = Column(String, unique=True, index=True)
    service_version = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AsteroidNeoWS(Base):
    """Asteroids - NeoWs (Near Earth Object Web Service)"""
    __tablename__ = "asteroids_neows"
    
    id = Column(Integer, primary_key=True, index=True)
    neo_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    nasa_jpl_url = Column(String)
    absolute_magnitude = Column(Float)
    estimated_diameter_min_m = Column(Float)
    estimated_diameter_max_m = Column(Float)
    is_potentially_hazardous = Column(Boolean, index=True)
    close_approach_date = Column(DateTime, nullable=True)
    close_approach_velocity_km_s = Column(Float, nullable=True)
    close_approach_distance_km = Column(Float, nullable=True)
    relative_velocity = Column(JSON)  # km/s, km/h, mph
    miss_distance = Column(JSON)  # km, miles, lunar, au
    orbiting_body = Column(String, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DONKI(Base):
    """DONKI (Space Weather Events & Alerts)"""
    __tablename__ = "donki"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    event_type = Column(String, index=True)  # "FLR", "SEP", "MPC", "RBE", "HSS", "CME"
    link_id = Column(String)
    activity_id = Column(String, nullable=True)
    peak_time = Column(DateTime, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    description = Column(Text)
    linked_events = Column(JSON)  # Related events
    source_location = Column(JSON, nullable=True)  # Solar coordinates
    active_region_number = Column(Integer, nullable=True)
    synoptic_sequence = Column(Integer, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EONET(Base):
    """EONET (Earth Observation Natural Events Tracking)"""
    __tablename__ = "eonet"
    
    id = Column(Integer, primary_key=True, index=True)
    eonet_id = Column(String, unique=True, index=True)
    event_type = Column(String, index=True)  # "Wildfires", "Floods", "Hurricanes", etc.
    event_title = Column(String)
    description = Column(Text, nullable=True)
    closed = Column(Boolean, default=False)
    geometry = Column(JSON)  # GeoJSON
    sources = Column(JSON)  # Data sources
    categories = Column(JSON)  # Event categories
    last_update = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EPIC(Base):
    """EPIC (Earth Polychromatic Imaging Camera)"""
    __tablename__ = "epic"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)
    caption = Column(String)
    image_name = Column(String, index=True)
    centroid_coordinates = Column(JSON)  # lat, lon
    dscovr_j2000_position = Column(JSON)  # x, y, z
    lunar_j2000_position = Column(JSON)  # x, y, z
    sun_j2000_position = Column(JSON)  # x, y, z
    attitude_quaternions = Column(JSON)  # Spacecraft orientation
    instrument = Column(String)  # "EPIC 1" or "EPIC 2"
    observation_date = Column(DateTime, index=True)
    url = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Exoplanet(Base):
    """Exoplanet Archive (Confirmed Exoplanets)"""
    __tablename__ = "exoplanets"
    
    id = Column(Integer, primary_key=True, index=True)
    pl_name = Column(String, unique=True, index=True)
    hostname = Column(String, index=True)
    pl_type = Column(String)  # Planet type classification
    pl_mass = Column(Float, nullable=True)  # Earth masses
    pl_radius = Column(Float, nullable=True)  # Earth radii
    pl_period = Column(Float, nullable=True)  # Orbital period (days)
    pl_semimajor_axis = Column(Float, nullable=True)  # AU
    pl_equilibrium_temp = Column(Float, nullable=True)  # Kelvin
    sy_distance = Column(Float, nullable=True)  # Parsecs
    st_teff = Column(Float, nullable=True)  # Star effective temp
    st_mass = Column(Float, nullable=True)  # Star mass (solar masses)
    st_radius = Column(Float, nullable=True)  # Star radius (solar radii)
    discovery_year = Column(Integer, nullable=True)
    discovery_method = Column(String, nullable=True)
    habitable_zone = Column(Boolean, default=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GIBS(Base):
    """GIBS (Global Imagery Browse Services)"""
    __tablename__ = "gibs"
    
    id = Column(Integer, primary_key=True, index=True)
    layer_name = Column(String, index=True)
    product_type = Column(String)  # "corrected_reflectance", "sea_ice", "snow", etc.
    description = Column(Text, nullable=True)
    projection = Column(String)  # "geographic", "web_mercator", etc.
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    image_url = Column(String)
    tile_coordinates = Column(JSON)  # x, y, z
    image_metadata = Column(JSON)  # GIBS-specific metadata
    resolution = Column(String)  # "250m", "500m", "1km"
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class InSightWeather(Base):
    """InSight Mars Weather (Sol-by-sol weather data)"""
    __tablename__ = "insight_weather"
    
    id = Column(Integer, primary_key=True, index=True)
    sol = Column(Integer, unique=True, index=True)  # Mars day
    season = Column(String)  # Mars season
    ls = Column(Float)  # Solar longitude
    min_temp_c = Column(Float, nullable=True)
    max_temp_c = Column(Float, nullable=True)
    avg_pressure = Column(Float, nullable=True)
    wind_direction = Column(JSON, nullable=True)  # most_common, compass_point
    wind_speed = Column(JSON, nullable=True)  # max, avg
    atmospheric_opacity = Column(JSON, nullable=True)  # min, max, avg
    sunrise = Column(String, nullable=True)
    sunset = Column(String, nullable=True)
    earth_date = Column(DateTime, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NASAImageLibrary(Base):
    """NASA Image & Video Library (Images, videos, audio)"""
    __tablename__ = "nasa_image_library"
    
    id = Column(Integer, primary_key=True, index=True)
    nasa_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    keywords = Column(JSON)  # List of tags
    media_type = Column(String)  # "image", "video", "audio"
    location = Column(String, nullable=True)
    photographer = Column(String, nullable=True)
    date_created = Column(DateTime)
    center = Column(String)  # NASA center
    album = Column(JSON)  # Album info
    links = Column(JSON)  # Image URLs in different sizes
    preview_url = Column(String)
    data_last_updated = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OpenScience(Base):
    """Open Science Data Repository (Research datasets)"""
    __tablename__ = "open_science_data"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    discipline = Column(String)  # Research discipline
    doi = Column(String, unique=True, nullable=True)
    authors = Column(JSON)
    publication_date = Column(DateTime)
    keywords = Column(JSON)
    file_count = Column(Integer)
    file_size_bytes = Column(Integer)
    format_types = Column(JSON)  # Data formats
    access_level = Column(String)  # "public", "restricted"
    source_repository = Column(String)
    url = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SatelliteSituationCenter(Base):
    """Satellite Situation Center (Active satellites)"""
    __tablename__ = "satellite_situation_center"
    
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(String, unique=True, index=True)
    satellite_name = Column(String, index=True)
    sat_number = Column(String)
    mission_name = Column(String)
    organization = Column(String)
    country_of_registry = Column(String)
    launch_date = Column(DateTime)
    launch_site = Column(String)
    orbital_period_minutes = Column(Float, nullable=True)
    orbital_inclination = Column(Float, nullable=True)
    apogee_km = Column(Float, nullable=True)
    perigee_km = Column(Float, nullable=True)
    operational_status = Column(String)  # "operational", "testing", "inactive"
    primary_mission = Column(String)
    position = Column(JSON, nullable=True)  # Current lat, lon, altitude
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CNEOS(Base):
    """SSD / CNEOS (Planetary Defense Center)"""
    __tablename__ = "cneos"
    
    id = Column(Integer, primary_key=True, index=True)
    designation = Column(String, unique=True, index=True)
    object_name = Column(String, index=True)
    object_type = Column(String)  # "asteroid", "comet", "NEO"
    epoch = Column(DateTime)
    semi_major_axis = Column(Float)
    eccentricity = Column(Float)
    inclination = Column(Float)
    longitude_ascending_node = Column(Float)
    argument_perihelion = Column(Float)
    mean_anomaly = Column(Float)
    perihelion_distance = Column(Float)
    aphelion_distance = Column(Float)
    orbital_period = Column(Float)  # Earth days
    diameter_km = Column(Float, nullable=True)
    absolute_magnitude = Column(Float)
    hazard_assessment = Column(String)  # Risk level
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TechPort(Base):
    """TechPort (NASA Technology Projects)"""
    __tablename__ = "techport"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String)  # "Active", "Completed", "On Hold"
    technology_maturity_level = Column(Integer)  # TRL 1-9
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    organization = Column(String)
    program = Column(String)
    mission = Column(String, nullable=True)
    benefits = Column(JSON)  # Expected benefits
    goals = Column(JSON)  # Project goals
    url = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TechTransfer(Base):
    """TechTransfer (NASA Spinoff Technologies)"""
    __tablename__ = "techtransfer"
    
    id = Column(Integer, primary_key=True, index=True)
    spinoff_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    benefits = Column(Text)
    category = Column(String)
    year_first_published = Column(Integer)
    year_updated = Column(Integer, nullable=True)
    agency = Column(String)
    organization = Column(String)
    application = Column(String)
    nasa_center = Column(String)
    status = Column(String)
    url = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TLE(Base):
    """TLE API (Satellite Tracking - Two-Line Elements)"""
    __tablename__ = "tle"
    
    id = Column(Integer, primary_key=True, index=True)
    satellite_number = Column(String, unique=True, index=True)
    satellite_name = Column(String, index=True)
    epoch = Column(DateTime)  # TLE epoch
    tle_line0 = Column(String)  # Satellite name
    tle_line1 = Column(String)  # Orbital elements line 1
    tle_line2 = Column(String)  # Orbital elements line 2
    inclination = Column(Float)  # Degrees
    raan = Column(Float)  # Right ascension of ascending node
    eccentricity = Column(Float)
    argument_perigee = Column(Float)  # Degrees
    mean_anomaly = Column(Float)  # Degrees
    mean_motion = Column(Float)  # Revolutions per day
    epoch_year = Column(Integer)
    epoch_day = Column(Float)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrekWMS(Base):
    """Trek WMS (Vesta, Moon, Mars Imagery - Web Map Service)"""
    __tablename__ = "trek_wms"
    
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, index=True)  # "Moon", "Mars", "Vesta"
    product_name = Column(String, index=True)
    layer_identifier = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    style = Column(String)
    crs = Column(String)  # Coordinate reference system
    bbox = Column(JSON)  # Bounding box: minx, miny, maxx, maxy
    image_url = Column(String)
    transparent = Column(Boolean)
    opaque = Column(Boolean)
    queryable = Column(Boolean)
    metadata_url = Column(String, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
