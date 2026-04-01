from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.weather import get_weather_forecast
from app.services.planner import generate_itinerary

router = APIRouter()

@router.post("/api/plan")
async def plan_trip(request: Request):
    data = await request.json()

    destination = data.get("destination")
    city = data.get("city")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    group_type = data.get("group_type")
    budget = data.get("budget")
    vibes = data.get("vibes", [])
    accommodation = data.get("accommodation", "")

    # Get weather forecast
    weather = await get_weather_forecast(city, check_in, check_out)

    # Generate itinerary
    itinerary = await generate_itinerary(
        destination=destination,
        city=city,
        check_in=check_in,
        check_out=check_out,
        group_type=group_type,
        budget=budget,
        vibes=vibes,
        accommodation=accommodation,
        weather=weather
    )

    return JSONResponse({"itinerary": itinerary, "weather": weather})
