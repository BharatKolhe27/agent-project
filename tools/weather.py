import requests


def get_weather(city: str):
    """
    Get the current weather for a city.

    Use when the user asks about:

    - Weather
    - Temperature
    - Climate
    - Forecast
    - Current conditions

    Examples:

    User:
    What's the weather in Pune?

    User:
    Tell me the temperature in Mumbai.

    User:
    Is it hot in Delhi today?

    Required Arguments:

    city:
        Name of the city.

    Returns:

    {
        "status": "success",
        "city": "Pune",
        "temperature": 26.3
    }

    or

    {
        "status": "error",
        "message": "city not found"
    }
    """
    if not city or not city.strip():

        return {
            "status": "error",
            "message": "city is required"
        }

    try:

        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1
            },
            timeout=10
        )

        geo.raise_for_status()

        geo = geo.json()

        if "results" not in geo:

            return {
                "status": "error",
                "message": f"city '{city}' not found"
            }

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m"
            },
            timeout=10
        )

        weather.raise_for_status()

        weather = weather.json()

        return {
            "status": "success",
            "city": city,
            "temperature":
                weather["current"]["temperature_2m"]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }