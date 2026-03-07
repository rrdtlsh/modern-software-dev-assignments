from api_client import (
    get_current_weather,
    get_weather_forecast,
    WeatherAPIError,
)


def register_tools(mcp):
    @mcp.tool()
    def get_current_weather_tool(city: str) -> dict:
        """
        Get current weather for a given city.
        """
        if not isinstance(city, str):
            return {"error": "City must be a string"}

        if not city.strip():
            return {"error": "City must not be empty"}

        try:
            return get_current_weather(city)
        except WeatherAPIError as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_weather_forecast_tool(city: str) -> dict:
        """
        Get 3-day weather forecast for a given city.
        """
        if not isinstance(city, str):
            return {"error": "City must be a string"}

        if not city.strip():
            return {"error": "City must not be empty"}

        try:
            return get_weather_forecast(city)
        except WeatherAPIError as e:
            return {"error": str(e)}