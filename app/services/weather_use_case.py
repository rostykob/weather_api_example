from datetime import datetime
from ..domain.entities import WeatherData, WeatherLogEntry
from ..domain.interfaces import WeatherService, CacheRepository, LogRepository


class GetWeatherUseCase:
    def __init__(
        self,
        weather_service: WeatherService,
        cache_repository: CacheRepository,
        log_repository: LogRepository,
    ):
        self.weather_service = weather_service
        self.cache_repository = cache_repository
        self.log_repository = log_repository

    async def execute(self, city: str) -> WeatherData:
        # Try to get from cache first
        cached_data = await self.cache_repository.get_cached_weather(city)
        if cached_data:
            await self._log_request(city, "cache", "success")
            return cached_data

        # Fetch from external service
        weather_data = await self.weather_service.fetch_weather(city)
        # Cache the new data
        await self.cache_repository.cache_weather(weather_data)
        # Log the request
        await self._log_request(city, "api", "success")
        return weather_data

    async def _log_request(self, city: str, source: str, status: str):
        log_entry = WeatherLogEntry(
            city=city,
            timestamp=datetime.now(),
            storage_path=f"{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            status=status,
        )
        await self.log_repository.log_weather_request(log_entry)
