import os
from datetime import datetime
import aiohttp
from fastapi import HTTPException
from ..domain.interfaces import WeatherService
from ..domain.entities import WeatherData
from ..config.settings import get_settings


class OpenWeatherMapService(WeatherService):
    def __init__(self):
        self.api_key = get_settings().WEATHER_API_KEY
        self.base_url = get_settings().WEATHER_API_URL

    async def fetch_weather(self, city: str) -> WeatherData:
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail="Failed to fetch weather data",
                    )
                data = await response.json()
                return WeatherData(
                    city=city,
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    description=data["weather"][0]["description"],
                    timestamp=datetime.now(),
                    source="api",
                    raw_data=data,
                )
