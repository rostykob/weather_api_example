from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class WeatherData:
    city: str
    temperature: float
    humidity: float
    description: str
    timestamp: datetime
    source: str  # 'cache' or 'api'
    raw_data: dict

@dataclass
class WeatherLogEntry:
    city: str
    timestamp: datetime
    storage_path: str
    status: str