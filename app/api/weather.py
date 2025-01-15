from fastapi import FastAPI, HTTPException, Query, APIRouter, Depends
from ..services.weather_use_case import GetWeatherUseCase
from ..infrastructure.weather_service import OpenWeatherMapService
from ..infrastructure.repositories import (
    FileSystemCacheRepository,
    FileSystemLogRepository,
)


router = APIRouter()


@router.get("/weather")
async def get_weather(
    city: str = Query(
        ...,
        description="City name to get weather for",
        pattern=r"^[a-zA-Z\u0600-\u06ff]+$",
    ),
    weather_service: OpenWeatherMapService = Depends(OpenWeatherMapService),
    cache_repository: FileSystemCacheRepository = Depends(FileSystemCacheRepository),
    log_repository: FileSystemLogRepository = Depends(FileSystemLogRepository),
):
    """Get weather data for a specific city."""
    try:
        city = city.lower()
        weather_use_case = GetWeatherUseCase(
            weather_service=weather_service,
            cache_repository=cache_repository,
            log_repository=log_repository,
        )
        weather_data = await weather_use_case.execute(city)
        return {"data": weather_data.raw_data, "source": weather_data.source}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
