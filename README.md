# Wayo

An AI-powered travel planning assistant for the Caribbean and Latin America. Users describe their trip and Wayo generates personalized itineraries, destination recommendations, and travel tips powered by the OpenAI API.

**Live app:** [wayo-zdgf.onrender.com](https://wayo-zdgf.onrender.com)

---

## Features

- Natural language trip planning — describe your trip in plain English or Spanish
- AI-generated itineraries tailored to destination, budget, and travel style
- Caribbean and Latin America focus
- Bilingual support (English / Spanish)
- Clean, responsive UI

## Tech Stack

**Backend:** FastAPI · Python · OpenAI API (GPT-4o)  
**Frontend:** Jinja2 · HTML · CSS · JavaScript  
**Hosting:** Render

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Keila0323/Wayo.git
cd Wayo

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# Run the app
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.
