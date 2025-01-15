from fastapi import FastAPI
from pathlib import Path
from .api import weather
from .config.settings import get_settings

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    debug=get_settings().DEBUG,
    openapi_url=f"{get_settings().API_V1_PREFIX}/openapi.json",
    docs_url=f"{get_settings().API_V1_PREFIX}/docs",
)

# Configuration
WEATHER_API_KEY = "f8fecedfbb6363fc3842fc549201ccd1"  # os.getenv("WEATHER_API_KEY", "your_api_key_here")
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
DATA_DIR = Path("data")
CACHE_EXPIRY = 300  # 5 minutes in seconds

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


app.router.include_router(weather.router)
