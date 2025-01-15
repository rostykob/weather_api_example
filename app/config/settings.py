from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from pathlib import Path


class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Weather API Service"
    DEBUG: bool = False

    # Weather API Settings
    WEATHER_API_KEY: str = Field(..., description="OpenWeatherMap API key")
    WEATHER_API_URL: str = "http://api.openweathermap.org/data/2.5/weather"
    WEATHER_API_UNITS: str = "metric"

    # Storage Settings
    DATA_DIR: Path = Field(default=Path("data"))
    CACHE_EXPIRY: int = Field(default=300, description="Cache expiry time in seconds")

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    @field_validator("DATA_DIR", mode="before")
    def create_data_dir(cls, v):
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return path

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
