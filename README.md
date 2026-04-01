# Wayo 🌴
### Plan less. Experience more.

Wayo is an AI-powered travel planner built specifically for the Caribbean and Latin America. Tell Wayo where you're going, your travel style, and your dates — and it builds a personalized day-by-day itinerary with restaurant recommendations, activities, nightlife, excursions, and local transport options.

**Weather-aware:** Sunny days get outdoor beaches and excursions. Rainy days get indoor museums, local markets, and cozy restaurants.

---

## Destinations

- 🇩🇴 Dominican Republic — Santo Domingo, Punta Cana, Santiago, Puerto Plata, Samaná
- 🇵🇷 Puerto Rico — San Juan, Ponce, Rincón, Vieques, Culebra
- 🇨🇴 Colombia — Cartagena, Medellín, Bogotá, Santa Marta, Cali
- 🇲🇽 Mexico — Mexico City, Cancún, Tulum, Oaxaca, Puerto Vallarta, Playa del Carmen

---

## Tech Stack

- **Backend:** FastAPI, Python 3.11
- **AI:** OpenAI GPT-4o
- **Weather:** OpenWeatherMap API
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render

---

## Setup

```bash
git clone https://github.com/Keila0323/Wayo.git
cd Wayo
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in your browser.

---

## Environment Variables

```
OPENAI_API_KEY=your_openai_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
PYTHON_VERSION=3.11.9
```

> The app works without API keys using mock data — great for development.

---

## Features

- AI-generated day-by-day itineraries tailored to your vibe
- Weather-aware activity recommendations (outdoor vs. indoor)
- Local transport guide for every city (Uber, metro, buses, walking)
- Accommodation-aware suggestions based on your neighborhood
- Group type filtering — solo, couple, family, adults only
- Budget tiers — budget, moderate, luxury

Built by Keila Olaverria
