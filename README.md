# Weather API Service

A FastAPI-based weather service that provides weather information for cities with caching capabilities.

## Features

- Asynchronous weather data fetching from OpenWeatherMap API
- Local file-based caching with 5-minute expiry
- Event logging (simulating DynamoDB)
- Docker support for easy deployment

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- OpenWeatherMap API key

## Local Setup

1. Clone the repository:
```bash
git clone 
cd weather-api
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export WEATHER_API_KEY=your_api_key_here
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8001

## Docker Deployment

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

The API will be available at http://localhost:8001

## API Usage

### Get Weather Data

```http
GET /weather?city=London
```

Query Parameters:
- `city` (required): Name of the city to get weather data for

Response:
```json
{
  "data": {
    "weather data here..."
  },
  "source": "api|cache"
}
```

## Architecture

The service implements:
- FastAPI for the web framework
- Asynchronous programming with `asyncio` and `aiohttp`
- Local file-based storage (simulating S3)
- JSON-based logging (simulating DynamoDB)
- 5-minute caching mechanism

## Error Handling

The service includes comprehensive error handling for:
- Invalid city names
- API failures
- Storage/retrieval errors
- Cache management issues

## Future Improvements

- Implement actual AWS S3 integration
- Add actual DynamoDB integration
- Add metrics and monitoring
- Implement rate limiting
- Add authentication
- Add more weather data endpoints