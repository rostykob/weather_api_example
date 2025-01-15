import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import aiofiles
from ..domain.interfaces import CacheRepository, LogRepository
from ..domain.entities import WeatherData, WeatherLogEntry
from ..config.settings import get_settings


class FileSystemCacheRepository(CacheRepository):
    def __init__(self):
        self.cache_dir = get_settings().DATA_DIR
        self.cache_expiry = get_settings().CACHE_EXPIRY
        self.cache_dir.mkdir(exist_ok=True)

    async def get_cached_weather(self, city: str) -> Optional[WeatherData]:
        try:
            files = [f for f in self.cache_dir.glob(f"{city}_*.json")]
            if not files:
                return None
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            file_age = datetime.now().timestamp() - latest_file.stat().st_mtime
            if file_age > self.cache_expiry:
                return None
            async with aiofiles.open(latest_file, mode="r") as f:
                content = await f.read()
                data = json.loads(content)
                return WeatherData(
                    city=city,
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    description=data["weather"][0]["description"],
                    timestamp=datetime.fromtimestamp(latest_file.stat().st_mtime),
                    source="cache",
                    raw_data=data,
                )
        except Exception:
            return None

    async def cache_weather(self, weather_data: WeatherData) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{weather_data.city}_{timestamp}.json"
        filepath = self.cache_dir / filename
        async with aiofiles.open(filepath, mode="w") as f:
            await f.write(json.dumps(weather_data.raw_data))


class FileSystemLogRepository(LogRepository):
    def __init__(self):
        self.log_dir = get_settings().DATA_DIR / "logs"
        self.log_file = self.log_dir / "weather_logs.json"
        self.log_dir.mkdir(exist_ok=True)

    async def log_weather_request(self, log_entry: WeatherLogEntry) -> None:
        try:
            if self.log_file.exists():
                async with aiofiles.open(self.log_file, mode="r") as f:
                    content = await f.read()
                    logs = json.loads(content)
            else:
                logs = []

            logs.append(
                {
                    "city": log_entry.city,
                    "timestamp": log_entry.timestamp.isoformat(),
                    "storage_path": log_entry.storage_path,
                    "status": log_entry.status,
                }
            )

            async with aiofiles.open(self.log_file, mode="w") as f:
                await f.write(json.dumps(logs, indent=2))
        except Exception as e:
            print(f"Error logging event: {e}")
