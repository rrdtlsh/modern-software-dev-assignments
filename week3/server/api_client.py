import requests
from typing import Dict, Any
from models import Coordinates
import logging

logger = logging.getLogger("weather-mcp.api")

BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass


def _handle_http_error(exc: requests.exceptions.HTTPError, context: str) -> None:
    status_code = None
    if exc.response is not None:
        status_code = exc.response.status_code

    if status_code == 429:
        logger.warning(f"{context} API rate limit exceeded (429)")
        raise WeatherAPIError(
            "API rate limit exceeded. Please try again later."
        ) from exc

    logger.error(f"{context} HTTP error {status_code}: {exc}")
    raise WeatherAPIError(
        f"{context} HTTP error (status {status_code}): {exc}"
    ) from exc


def get_coordinates(city: str) -> Coordinates:
    logger.info(f"Fetching coordinates for city: {city}")

    try:
        response = requests.get(
            GEOCODE_URL,
            params={"name": city, "count": 1},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "results" not in data or not data["results"]:
            logger.warning(f"No geocoding results for city: {city}")
            raise WeatherAPIError(f"No results found for city: {city}")

        result = data["results"][0]

        if "latitude" not in result or "longitude" not in result:
            logger.error("Invalid geocoding response structure")
            raise WeatherAPIError("Invalid geocoding response structure")

        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
        }

    except requests.exceptions.Timeout:
        logger.warning("Geocoding request timed out")
        raise WeatherAPIError("Geocoding request timed out")

    except requests.exceptions.HTTPError as exc:
        _handle_http_error(exc, "Geocoding")

    except requests.exceptions.RequestException as exc:
        logger.error(f"Geocoding request failed: {exc}")
        raise WeatherAPIError(f"Geocoding request failed: {exc}") from exc


def get_current_weather(city: str) -> Dict[str, Any]:
    logger.info(f"Fetching current weather for city: {city}")

    coords = get_coordinates(city)

    try:
        response = requests.get(
            BASE_URL,
            params={
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "current_weather": True,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "current_weather" not in data:
            logger.error("Weather data not available in response")
            raise WeatherAPIError("Weather data not available")

        return data["current_weather"]

    except requests.exceptions.Timeout:
        logger.warning("Weather request timed out")
        raise WeatherAPIError("Weather request timed out")

    except requests.exceptions.HTTPError as exc:
        _handle_http_error(exc, "Weather")

    except requests.exceptions.RequestException as exc:
        logger.error(f"Weather request failed: {exc}")
        raise WeatherAPIError(f"Weather request failed: {exc}") from exc


def get_weather_forecast(city: str) -> Dict[str, Any]:
    logger.info(f"Fetching 3-day forecast for city: {city}")

    coords = get_coordinates(city)

    try:
        response = requests.get(
            BASE_URL,
            params={
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min",
                "forecast_days": 3,
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "daily" not in data:
            logger.error("Forecast data not available in response")
            raise WeatherAPIError("Forecast data not available")

        return data["daily"]

    except requests.exceptions.Timeout:
        logger.warning("Forecast request timed out")
        raise WeatherAPIError("Forecast request timed out")

    except requests.exceptions.HTTPError as exc:
        _handle_http_error(exc, "Forecast")

    except requests.exceptions.RequestException as exc:
        logger.error(f"Forecast request failed: {exc}")
        raise WeatherAPIError(f"Forecast request failed: {exc}") from exc