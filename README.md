# Wayo 🌴
### Plan less. Experience more.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai&logoColor=white)
![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)

Wayo is an AI-powered travel planner built specifically for the **Caribbean and Latin America**. Tell Wayo where you're going, your travel style, and your dates — and it builds a personalized day-by-day itinerary with restaurant picks, activities, nightlife, excursions, and local transport options.

> **Weather-aware:** Sunny days get outdoor beaches and excursions. Rainy days get indoor museums, local markets, and cozy spots.

---

## Why I Built This

Most travel apps focus on Europe and North America. The Caribbean and Latin America are treated as an afterthought — generic suggestions, no local context, no cultural depth. I built Wayo to fix that, starting with the destinations I know best. It's also the project where I went from "I can write Python" to "I can architect and ship a full-stack AI product."

---

## Live Demo

🔗 **[Try Wayo](https://wayo-travel.onrender.com)** *(hosted on Render — may take ~30s to wake up on first load)*

---

## Features

- AI-generated day-by-day itineraries tailored to your vibe
- Weather-aware activity recommendations (outdoor vs. indoor)
- Local transport guide for every city (Uber, metro, buses, walking)
- Accommodation-aware suggestions based on your neighborhood
- Group type filtering — solo, couple, family, adults only
- Budget tiers — budget, moderate, luxury
- Bilingual support — English & Spanish

---

## Destinations

| Country | Cities |
|---------|--------|
| 🇩🇴 Dominican Republic | Santo Domingo, Punta Cana, Santiago, Puerto Plata, Samaná |
| 🇵🇷 Puerto Rico | San Juan, Ponce, Rincón, Vieques, Culebra |
| 🇨🇴 Colombia | Cartagena, Medellín, Bogotá, Santa Marta, Cali |
| 🇲🇽 Mexico | Mexico City, Cancún, Tulum, Oaxaca, Puerto Vallarta |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python 3.11) |
| AI | OpenAI GPT-4o |
| Weather | OpenWeatherMap API |
| Frontend (this repo) | HTML, CSS, JavaScript |
| Frontend (Next.js) | [Wayo-Next](https://github.com/Keila0323/Wayo-Next) — TypeScript, Next.js 14, Tailwind CSS, shadcn/ui |
| Deployment | Render |

---

## Architecture

```
Wayo/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── routers/         # Route handlers (itinerary, weather, etc.)
│   ├── services/        # AI + weather service logic
│   ├── static/          # CSS, JS, images
│   └── templates/       # Jinja2 HTML templates
├── requirements.txt
└── .env.example
```

---

## Setup

```bash
git clone https://github.com/Keila0323/Wayo.git
cd Wayo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn app.main:app --reload
```

Open `http://localhost:8000` in your browser.

### Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

> The app runs with mock data if no API keys are provided — great for local development.

---

## Related Repo

**[Wayo-Next](https://github.com/Keila0323/Wayo-Next)** — Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui frontend, connecting to this FastAPI backend.

---

Built by [Keila Olaverria](https://www.linkedin.com/in/keila-olaverria-56661493/) · Boston, MA
