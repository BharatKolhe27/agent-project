import requests


def get_weather(city: str):

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