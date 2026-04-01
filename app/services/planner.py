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

MOCK_RECOMMENDATIONS = {
    "gastronomy": {
        "food": [
            {"name": "La Bandera Dominicana", "type": "food", "subcategory": "Local Dish", "description": "The iconic Dominican plate — rice, beans, and your choice of meat. Best found at a local comedor (family kitchen) rather than a tourist restaurant.", "vibe": "Authentic", "cost": "$", "transport": "Ask your hotel for the nearest comedor"},
            {"name": "Mangú con Los Tres Golpes", "type": "food", "subcategory": "Street Food", "description": "Mashed plantains topped with sautéed onions, fried cheese, salami, and eggs. A classic Dominican breakfast you can find everywhere.", "vibe": "Local favorite", "cost": "$", "transport": "Any local café or street stand"},
            {"name": "Fresh Coconut Water", "type": "food", "subcategory": "Street Food", "description": "Street vendors sell fresh coconuts all over — cut open and handed to you. Ice cold and refreshing, especially at the beach.", "vibe": "Casual", "cost": "$", "transport": "Beach vendors or market stalls"},
        ],
        "drinks": [
            {"name": "Mamajuana", "type": "drinks", "subcategory": "Local Spirit", "description": "The Dominican Republic's legendary herbal rum drink — a mix of rum, red wine, and honey soaked with tree bark and herbs. Every family has their own recipe.", "vibe": "Cultural", "cost": "$$", "transport": "Any local bar or restaurant"},
            {"name": "Morir Soñando", "type": "drinks", "subcategory": "Local Drink", "description": "Literally translates to 'die dreaming' — a refreshing mix of orange juice and evaporated milk. Sounds strange, tastes incredible.", "vibe": "Sweet & refreshing", "cost": "$", "transport": "Juice stands and local cafés"},
        ],
        "bars": [
            {"name": "Malecón Sunset Strip", "type": "bars", "subcategory": "Outdoor Bar", "description": "The famous waterfront boulevard comes alive at sunset. Open-air bars line the strip — grab a Presidente beer and watch the Caribbean Sea turn gold.", "vibe": "Lively", "cost": "$$", "transport": "Uber to Malecón (~10 min from most hotels)"},
            {"name": "Local Colmado Bar", "type": "bars", "subcategory": "Neighborhood Bar", "description": "Every neighborhood has a colmado — a corner store that doubles as a bar. Pull up a plastic chair, order a cold beer, and experience real Dominican social life.", "vibe": "Authentic local", "cost": "$", "transport": "Walk — they're everywhere"},
        ],
        "restaurants": [
            {"name": "Seafood by the Water", "type": "restaurants", "subcategory": "Seafood", "description": "Fresh catch of the day — grilled fish, shrimp, and lobster served with tostones and rice. Best found at beachside spots outside the resort zones.", "vibe": "Fresh & local", "cost": "$$", "transport": "Uber or rental car (~15-20 min)"},
            {"name": "Chinatown District", "type": "restaurants", "subcategory": "Fusion", "description": "Santo Domingo has a vibrant Chinese-Dominican food scene. Try chofán — Dominican-style fried rice that's become a local staple.", "vibe": "Unique fusion", "cost": "$", "transport": "Uber to Barrio Chino (~15 min)"},
        ]
    },
    "activities": {
        "activities": [
            {"name": "Whale Watching in Samaná", "type": "activities", "subcategory": "Nature", "description": "Every January-March, humpback whales migrate to Samaná Bay — one of the largest whale watching destinations in the world. Boats depart from the town dock.", "vibe": "Once in a lifetime", "cost": "$$$", "transport": "3-hour drive from Santo Domingo or 1-hour flight"},
            {"name": "27 Waterfalls of Damajagua", "type": "activities", "subcategory": "Adventure", "description": "Jump, slide, and swim through a series of turquoise waterfalls in the jungle. One of the most thrilling experiences in the Caribbean — guide required.", "vibe": "Adventure", "cost": "$$", "transport": "45 min from Puerto Plata"},
        ],
        "beaches": [
            {"name": "Playa Rincón", "type": "beaches", "subcategory": "Beach", "description": "Consistently ranked one of the best beaches in the Caribbean. Pristine white sand, crystal water, and almost no development. Only accessible by boat or 4x4.", "vibe": "Secluded paradise", "cost": "$$", "transport": "Boat from Las Galeras (~30 min)"},
            {"name": "Bávaro Beach", "type": "beaches", "subcategory": "Beach", "description": "The postcard-perfect beach of Punta Cana — 32km of white sand and turquoise water. Early mornings are peaceful before the resort crowds arrive.", "vibe": "Classic Caribbean", "cost": "Free (or resort fee)", "transport": "Walking from most Punta Cana resorts"},
        ],
        "landmarks": [
            {"name": "Zona Colonial, Santo Domingo", "type": "landmarks", "subcategory": "Historic", "description": "The oldest continuously inhabited European city in the Americas. Walk the cobblestone streets, visit the first cathedral built in the New World, and explore centuries of history.", "vibe": "Historic & cultural", "cost": "Free to walk", "transport": "Uber to Zona Colonial (~20 min from most hotels)"},
            {"name": "Fortaleza Ozama", "type": "landmarks", "subcategory": "Historic", "description": "The oldest European fortress in the Americas, built in 1502. Climb the tower for panoramic views of the Ozama River and the colonial city.", "vibe": "Historic", "cost": "$", "transport": "Inside Zona Colonial — walking distance"},
        ],
        "experiences": [
            {"name": "Bachata & Merengue Night", "type": "experiences", "subcategory": "Nightlife", "description": "Merengue is the heartbeat of the Dominican Republic. Find a local dance hall on a Friday or Saturday night — locals will teach you the steps.", "vibe": "Cultural nightlife", "cost": "$$", "transport": "Uber to local venue"},
            {"name": "Local Baseball Game", "type": "experiences", "subcategory": "Sports", "description": "Baseball is a religion in the DR. Catching a winter league game is one of the most authentic cultural experiences you can have — loud, passionate, and incredibly fun.", "vibe": "Authentic local", "cost": "$", "transport": "Uber to Estadio Quisqueya (~15 min)"},
        ]
    },
    "transport": {},
    "tips": [
        "Always carry small bills in local currency for street food and taxis",
        "Download the Uber app before you arrive",
        "Bargain respectfully at local markets — it's expected",
        "Try the street food — it's often the most authentic option"
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
    """Generate curated recommendations using OpenAI or mock data."""

    transport = TRANSPORT_INFO.get(city, {
        "options": ["Uber (widely available)", "Local taxis", "Walking"],
        "tip": "Uber is available in most major cities. Ask your hotel for local transport advice."
    })

    if not os.getenv("OPENAI_API_KEY"):
        result = dict(MOCK_RECOMMENDATIONS)
        result["transport"] = transport
        result["city"] = city
        result["destination"] = destination
        result["group_type"] = group_type
        result["budget"] = budget
        result["vibes"] = vibes
        result["weather"] = weather
        return result

    vibe_str = ", ".join(vibes) if vibes else "general sightseeing"
    weather_note = ""
    if weather:
        sunny_days = sum(1 for w in weather if w.get("is_sunny"))
        rainy_days = len(weather) - sunny_days
        weather_note = f"{sunny_days} sunny days, {rainy_days} rainy days forecast."

    prompt = f"""You are Wayo, an expert local guide for Latin America and the Caribbean.

Generate curated local recommendations for a traveler visiting {city}, {destination}.

TRIP DETAILS:
- Destination: {city}, {destination}
- Dates: {check_in} to {check_out}
- Group type: {group_type}
- Budget level: {budget}
- Interests: {vibe_str}
- Staying near: {accommodation if accommodation else "city center"}
- Weather: {weather_note}

Generate 3-5 recommendations for EACH of these 8 subcategories:
1. food — local dishes and street food
2. drinks — local beverages, juices, spirits
3. bars — bars, nightlife spots, lounges
4. restaurants — sit-down dining spots
5. activities — things to do, tours, adventures
6. beaches — beaches and waterfront spots
7. landmarks — historic sites, viewpoints, iconic places
8. experiences — cultural events, music, sports, unique local experiences

RULES:
- Use REAL, SPECIFIC place names and neighborhoods for {city}
- Tailor to {group_type} and {budget} budget
- Include both indoor and outdoor options (weather: {weather_note})
- Be authentic — local spots over tourist traps
- Each recommendation must have a name, short description (2 sentences max), vibe tag, cost estimate ($/$$/$$$ ), and how to get there

Return ONLY valid JSON in this exact format:
{{
  "city": "{city}",
  "destination": "{destination}",
  "group_type": "{group_type}",
  "budget": "{budget}",
  "gastronomy": {{
    "food": [
      {{"name": "...", "subcategory": "Local Dish|Street Food|Snack", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "drinks": [
      {{"name": "...", "subcategory": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "bars": [
      {{"name": "...", "subcategory": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "restaurants": [
      {{"name": "...", "subcategory": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ]
  }},
  "activities": {{
    "activities": [
      {{"name": "...", "subcategory": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "beaches": [
      {{"name": "...", "subcategory": "Beach", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "landmarks": [
      {{"name": "...", "subcategory": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "experiences": [
      {{"name": "...", "subcategory": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ]
  }},
  "transport": {{
    "options": {json.dumps(transport['options'])},
    "tip": "{transport['tip']}"
  }},
  "tips": ["tip1", "tip2", "tip3", "tip4"]
}}"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=4000
        )
        result = json.loads(response.choices[0].message.content)
        result["weather"] = weather
        return result
    except Exception as e:
        result = dict(MOCK_RECOMMENDATIONS)
        result["transport"] = transport
        result["error"] = str(e)
        result["weather"] = weather
        return result
