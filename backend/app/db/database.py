from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

settings = get_settings()

# Build a safe async DB URL for common cases (postgres -> asyncpg)
db_url = settings.DATABASE_URL or "sqlite+aiosqlite:///./spacescope.db"
if db_url.startswith("postgresql://") and "asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Async engine
engine = create_async_engine(
    db_url,
    echo=getattr(settings, "SQLALCHEMY_ECHO", False),
    future=True,
)

# Session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Declarative base for models
Base = declarative_base()


async def get_db():
    """Dependency for database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
