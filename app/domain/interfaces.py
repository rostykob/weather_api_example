from abc import ABC, abstractmethod
from typing import Optional
from .entities import WeatherData, WeatherLogEntry

class WeatherRepository(ABC):
    @abstractmethod
    async def get_weather(self, city: str) -> Optional[WeatherData]:
        pass

    @abstractmethod
    async def save_weather(self, weather_data: WeatherData) -> None:
        pass

class WeatherService(ABC):
    @abstractmethod
    async def fetch_weather(self, city: str) -> WeatherData:
        pass

class CacheRepository(ABC):
    @abstractmethod
    async def get_cached_weather(self, city: str) -> Optional[WeatherData]:
        pass

    @abstractmethod
    async def cache_weather(self, weather_data: WeatherData) -> None:
        pass

class LogRepository(ABC):
    @abstractmethod
    async def log_weather_request(self, log_entry: WeatherLogEntry) -> None:
        pass