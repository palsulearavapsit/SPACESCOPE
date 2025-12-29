from functools import lru_cache
import logging
from typing import Any
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger("app.core.config")


class Settings(BaseSettings):
    # --- Core ---
    DATABASE_URL: str = "sqlite+aiosqlite:///./spacescope.db"
    SECRET_KEY: str = "change-me"
    SQLALCHEMY_ECHO: bool = False

    # --- API metadata & behavior ---
    API_TITLE: str = "SpaceScope API"
    API_VERSION: str = "0.0.1"
    DEBUG: bool = False

    # --- AI ---
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_MAX_TOKENS: int = 2000

    # --- Celery ---
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list[str] = Field(default_factory=lambda: ["json"])
    CELERY_TIMEZONE: str = "UTC"

    # --- NASA / External keys ---
    NASA_API_KEY: str = ""

    # --- App behavior ---
    NASA_DATA_REFRESH_INTERVAL_HOURS: int = 6
    CACHE_TTL_SECONDS: int = 86400
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
        protected_namespaces=[],
    )

    def __getattr__(self, name: str) -> Any:
        # Backward-compatible lowercase access (settings.foo -> settings.FOO)
        # Never raise AttributeError for missing attributes; return None instead.
        upper = name.upper()
        try:
            return object.__getattribute__(self, upper)
        except AttributeError:
            return None

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting via lowercase names as an alias to uppercase fields
        if isinstance(name, str) and name.islower():
            name = name.upper()
        object.__setattr__(self, name, value)

    def __dir__(self) -> list[str]:
        # Include lowercase aliases in autocompletion
        entries = set(super().__dir__())
        for attr in list(entries):
            if isinstance(attr, str) and attr.isupper():
                entries.add(attr.lower())
        return sorted(entries)

    def _warn_defaults(self) -> None:
        # Helpful warnings when important values are left as safe defaults
        if self.SECRET_KEY in ("", "change-me"):
            logger.warning("SECRET_KEY not set or using insecure default - set SECRET_KEY in env")
        if not self.DATABASE_URL:
            logger.warning("DATABASE_URL not set - using sqlite in-tree fallback")
        if not self.CELERY_BROKER_URL:
            logger.warning("CELERY_BROKER_URL not set - Celery will use in-memory broker if available")


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    # Log helpful warnings instead of crashing when env vars are missing
    try:
        settings._warn_defaults()
    except Exception:
        # Avoid any crash from logging in config
        pass
    return settings
