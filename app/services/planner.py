import os
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

TRANSPORT_INFO = {
    "Santo Domingo": {
        "options": ["Uber (widely available)", "Metro Line 1 & 2 (~$0.35/ride)", "Carros públicos (shared taxis)", "Motoconcho (motorcycle taxi — adventurous!)"],
        "tip": "Uber is safest and easiest for tourists. Metro is great for crossing the city cheaply."
    },
    "Punta Cana": {
        "options": ["Uber (available)", "Resort shuttles", "Moto-taxi for short distances", "Rental car recommended for exploring"],
        "tip": "Most resorts are spread out — a rental car gives you freedom to explore local beaches."
    },
    "Santiago": {
        "options": ["Uber (available)", "Carros públicos", "Motoconcho"],
        "tip": "Carros públicos run fixed routes and are very cheap (~$0.50). Ask locals for routes."
    },
    "San Juan": {
        "options": ["Uber (widely available)", "AMA Bus (~$0.75/ride)", "Ferry to Cataño ($0.50)", "Walking in Old San Juan"],
        "tip": "Old San Juan is very walkable. Take the free trolley between city gates."
    },
    "Cartagena": {
        "options": ["Uber (available)", "Cabify", "Tuk-tuks in the old city", "Horse-drawn carriages (touristy but fun)", "Walking in Walled City"],
        "tip": "The Walled City is best explored on foot. Tuk-tuks are great for short hops."
    },
    "Medellín": {
        "options": ["Uber (available)", "Metro (~$0.80/ride)", "Metro Cable (connects hillside neighborhoods)", "Cabify"],
        "tip": "Medellín's Metro system is clean, safe, and affordable. The cable car gives stunning city views."
    },
    "Bogotá": {
        "options": ["Uber (available)", "TransMilenio BRT (~$0.70/ride)", "Cabify", "Bike share (BiciBogotá)"],
        "tip": "TransMilenio covers most of the city. Uber/Cabify are safer for nighttime travel."
    },
    "Mexico City": {
        "options": ["Uber (widely available)", "Metro (~$0.25/ride)", "Metrobús", "Cabify", "Walking in Roma/Condesa/Centro"],
        "tip": "Mexico City's metro is one of the cheapest in the world. Uber is reliable for late nights."
    },
    "Cancún": {
        "options": ["Uber (available)", "ADO Bus (to Tulum/Playa ~$8-15)", "R1/R2 local buses ($0.60)", "Rental car for flexibility"],
        "tip": "The hotel zone is long and walkable only in sections. Local R1/R2 buses run the full strip cheaply."
    },
    "Tulum": {
        "options": ["Rental bike or scooter (most popular)", "Uber (limited)", "Colectivos to Playa del Carmen (~$3)", "Rental car"],
        "tip": "Tulum's town and beach zone are 3km apart. Renting a bike or scooter is the most common way to get around."
    },
}

MOCK_ITINERARY = {
    "days": [
        {
            "day": "Day 1",
            "date": "Arrival & First Impressions",
            "weather_note": "☀️ Sunny & warm — perfect for settling in",
            "morning": {
                "title": "Arrive & Check In",
                "description": "Get settled at your accommodation, freshen up, and take a slow walk around your neighborhood to get oriented.",
                "type": "arrival",
                "transport": "Take Uber from the airport to your hotel (~20 min)"
            },
            "afternoon": {
                "title": "Explore the Old City",
                "description": "Head to the historic colonial zone for a self-guided walking tour. Stop at the main plaza, grab a fresh coconut from a street vendor, and soak in the architecture.",
                "type": "sightseeing",
                "transport": "Walk or take a 5-min Uber from your hotel"
            },
            "evening": {
                "title": "Dinner at a Local Spot",
                "description": "Try traditional cuisine at a family-run restaurant. Order the daily special — locals always know what's best that day.",
                "type": "dining",
                "transport": "Short walk or Uber (~$3)"
            }
        },
        {
            "day": "Day 2",
            "date": "Beach & Culture",
            "weather_note": "☀️ Another beautiful day — great for the beach",
            "morning": {
                "title": "Beach Morning",
                "description": "Head to the nearest beach early before it gets crowded. Bring snacks and enjoy the calm morning water.",
                "type": "beach",
                "transport": "Uber to beach (~15 min, ~$5)"
            },
            "afternoon": {
                "title": "Local Market",
                "description": "Visit the local market for handmade crafts, tropical fruits, and street food. A great place to pick up souvenirs and try local snacks.",
                "type": "culture",
                "transport": "Uber or local bus"
            },
            "evening": {
                "title": "Rooftop Bar",
                "description": "Catch the sunset from a rooftop bar. Order a local rum cocktail and enjoy the city views as the sky turns orange and pink.",
                "type": "nightlife",
                "transport": "Uber (~$4)"
            }
        }
    ],
    "tips": [
        "Always carry small bills in local currency for street food and taxis",
        "Download the Uber app before you arrive — it works in all 4 destinations",
        "Bargain respectfully at local markets — it's expected and part of the culture",
        "Try the street food — it's often the most authentic and delicious option"
    ]
}

async def generate_itinerary(
    destination: str,
    city: str,
    check_in: str,
    check_out: str,
    group_type: str,
    budget: str,
    vibes: list,
    accommodation: str,
    weather: list
) -> dict:
    """Generate a day-by-day itinerary using OpenAI or mock data."""

    transport = TRANSPORT_INFO.get(city, {
        "options": ["Uber (widely available)", "Local taxis", "Walking"],
        "tip": "Uber is available in most major cities. Ask your hotel for local transport advice."
    })

    if not os.getenv("OPENAI_API_KEY"):
        # Return mock data for development
        itinerary = dict(MOCK_ITINERARY)
        itinerary["transport"] = transport
        itinerary["city"] = city
        itinerary["destination"] = destination
        itinerary["group_type"] = group_type
        itinerary["budget"] = budget
        itinerary["vibes"] = vibes
        return itinerary

    # Build weather summary for prompt
    weather_summary = "\n".join([
        f"- {w['day']}: {w['icon']} {w['conditions']}, {w['temp']}°F — {'OUTDOOR activities recommended' if w['is_sunny'] else 'INDOOR activities recommended'}"
        for w in weather
    ])

    vibe_str = ", ".join(vibes) if vibes else "general sightseeing"

    prompt = f"""You are Wayo, an expert local travel guide for Latin America and the Caribbean.

Create a detailed day-by-day travel itinerary for the following trip:

TRIP DETAILS:
- Destination: {city}, {destination}
- Dates: {check_in} to {check_out} ({len(weather)} days)
- Group type: {group_type}
- Budget level: {budget}
- Interests/vibes: {vibe_str}
- Staying at/near: {accommodation if accommodation else "city center"}

WEATHER FORECAST:
{weather_summary}

TRANSPORT OPTIONS IN {city}:
{chr(10).join(f'- {opt}' for opt in transport['options'])}
Local tip: {transport['tip']}

RULES:
1. For SUNNY days: prioritize outdoor activities, beaches, excursions, walking tours, outdoor dining
2. For RAINY days: prioritize indoor activities — museums, cooking classes, indoor markets, spas, rooftop bars with covers, local restaurants
3. Each day has morning, afternoon, and evening sections
4. Include specific real restaurant names, neighborhoods, and attraction names for {city}
5. Add transport instructions for each activity (how to get there, cost estimate)
6. Tailor everything to the group type ({group_type}) and budget ({budget})
7. Include authentic local experiences, not just tourist traps
8. For nightlife vibes: include local bars, clubs, live music venues specific to {city}
9. For family vibes: include kid-friendly activities and family restaurants

Return ONLY valid JSON in this exact format:
{{
  "city": "{city}",
  "destination": "{destination}",
  "group_type": "{group_type}",
  "budget": "{budget}",
  "vibes": {json.dumps(vibes)},
  "days": [
    {{
      "day": "Day 1",
      "date": "Full date string",
      "weather_note": "Weather emoji + brief note",
      "morning": {{
        "title": "Activity name",
        "description": "2-3 sentences with specific details",
        "type": "beach|culture|food|nightlife|sightseeing|indoor|adventure",
        "transport": "How to get there + cost estimate"
      }},
      "afternoon": {{
        "title": "Activity name",
        "description": "2-3 sentences with specific details",
        "type": "beach|culture|food|nightlife|sightseeing|indoor|adventure",
        "transport": "How to get there + cost estimate"
      }},
      "evening": {{
        "title": "Activity name",
        "description": "2-3 sentences with specific details",
        "type": "beach|culture|food|nightlife|sightseeing|indoor|adventure",
        "transport": "How to get there + cost estimate"
      }}
    }}
  ],
  "tips": ["tip1", "tip2", "tip3", "tip4"],
  "transport": {{
    "options": {json.dumps(transport['options'])},
    "tip": "{transport['tip']}"
  }}
}}"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=3000
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        # Fall back to mock if API fails
        itinerary = dict(MOCK_ITINERARY)
        itinerary["transport"] = transport
        itinerary["error"] = str(e)
        return itinerary
