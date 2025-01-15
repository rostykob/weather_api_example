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


app.router.include_router(weather.router)
