import httpx
import os
from datetime import datetime, timedelta

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

CITY_COORDS = {
    "Santo Domingo": {"lat": 18.4861, "lon": -69.9312},
    "Punta Cana": {"lat": 18.5601, "lon": -68.3725},
    "Santiago": {"lat": 19.4517, "lon": -70.6970},
    "San Juan": {"lat": 18.4655, "lon": -66.1057},
    "Cartagena": {"lat": 10.3910, "lon": -75.4794},
    "Medellín": {"lat": 6.2442, "lon": -75.5812},
    "Bogotá": {"lat": 4.7110, "lon": -74.0721},
    "Mexico City": {"lat": 19.4326, "lon": -99.1332},
    "Cancún": {"lat": 21.1619, "lon": -86.8515},
    "Tulum": {"lat": 20.2114, "lon": -87.4654},
}

async def get_weather_forecast(city: str, check_in: str, check_out: str) -> list:
    """Get weather forecast for travel dates. Falls back to mock data if no API key."""
    
    if not WEATHER_API_KEY:
        return _mock_weather(city, check_in, check_out)

    coords = CITY_COORDS.get(city, {"lat": 18.4861, "lon": -69.9312})
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "appid": WEATHER_API_KEY,
                    "units": "imperial",
                    "cnt": 40
                }
            )
            data = resp.json()
            return _parse_forecast(data, check_in, check_out)
    except Exception:
        return _mock_weather(city, check_in, check_out)


def _parse_forecast(data: dict, check_in: str, check_out: str) -> list:
    start = datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.strptime(check_out, "%Y-%m-%d")
    days = (end - start).days

    daily = []
    for i in range(days):
        date = start + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Find forecast entries for this date
        entries = [f for f in data.get("list", []) if f["dt_txt"].startswith(date_str)]
        
        if entries:
            avg_temp = sum(e["main"]["temp"] for e in entries) / len(entries)
            conditions = entries[len(entries)//2]["weather"][0]["main"]
            desc = entries[len(entries)//2]["weather"][0]["description"]
        else:
            avg_temp = 82
            conditions = "Clear"
            desc = "sunny skies"

        is_sunny = conditions in ["Clear", "Clouds"] and "rain" not in desc.lower()
        
        daily.append({
            "date": date_str,
            "day": date.strftime("%A, %B %d"),
            "temp": round(avg_temp),
            "conditions": conditions,
            "description": desc,
            "is_sunny": is_sunny,
            "icon": "☀️" if is_sunny else "🌧️"
        })
    
    return daily


def _mock_weather(city: str, check_in: str, check_out: str) -> list:
    """Mock weather data for development (no API key needed)."""
    start = datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.strptime(check_out, "%Y-%m-%d")
    days = (end - start).days

    mock_patterns = [
        {"conditions": "Clear", "description": "sunny skies", "temp": 84, "is_sunny": True, "icon": "☀️"},
        {"conditions": "Clear", "description": "sunny skies", "temp": 86, "is_sunny": True, "icon": "☀️"},
        {"conditions": "Clouds", "description": "partly cloudy", "temp": 81, "is_sunny": True, "icon": "⛅"},
        {"conditions": "Rain", "description": "light rain showers", "temp": 77, "is_sunny": False, "icon": "🌧️"},
        {"conditions": "Clear", "description": "sunny skies", "temp": 85, "is_sunny": True, "icon": "☀️"},
        {"conditions": "Clouds", "description": "mostly cloudy", "temp": 79, "is_sunny": True, "icon": "⛅"},
        {"conditions": "Clear", "description": "clear and warm", "temp": 87, "is_sunny": True, "icon": "☀️"},
    ]

    daily = []
    for i in range(days):
        date = start + timedelta(days=i)
        pattern = mock_patterns[i % len(mock_patterns)]
        daily.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%A, %B %d"),
            **pattern
        })
    
    return daily
