# 🚀 SpaceScope — The AI × Space Intelligence Platform

**SpaceScope** is an AI-powered platform that aggregates, analyzes, and explains real-time space data — from sky events and missions to space weather and Earth impact — in a single intelligent interface.

It combines **live space data**, **machine intelligence**, and **educational tooling** to make space exploration understandable, actionable, and inspiring.

---

## 🧠 Why SpaceScope?

Space information today is:
- Scattered across many websites
- Hard to understand for non-experts
- Not connected to real-world impact

**SpaceScope solves this by:**
- Centralizing space data into one dashboard  
- Explaining complex phenomena using AI  
- Connecting space science with Earth applications (climate, disasters, satellites, etc.)

---

## ✨ Features

### 🌌 Space Intelligence
- Upcoming sky events (meteor showers, eclipses, ISS passes)
- Space weather alerts (solar flares, geomagnetic storms)
- Mission timelines and statuses

### 🤖 AI Layer
- Natural language chat for learning and exploration
- AI explanations for space phenomena
- Context-aware responses (missions, weather, learning)

### 🌍 Earth Impact
- Satellite-based environmental insights
- Climate, pollution, agriculture, and disaster monitoring

### 🎓 Learning Hub
- Educational articles and summaries
- Difficulty-based content
- Integrated quizzes

### ⚙️ Platform Features
- RESTful API
- Modular microservice backend
- Async task processing
- Fully dockerized deployment

---

## 🏗️ Architecture

```
Frontend (React + Vite + Tailwind)
        ↓
FastAPI Backend (REST API)
        ↓
PostgreSQL (Data)     Redis (Cache & Queue)
        ↓
Celery Workers (Async Tasks)
        ↓
External APIs (NASA, Gemini AI)
```

---

## 🛠 Tech Stack

### Languages
- Python
- JavaScript

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- Celery
- Redis

### Frontend
- React
- Vite
- Tailwind CSS
- Axios

### Database
- PostgreSQL

### APIs
- Google Gemini API
- NASA Open APIs

### Infrastructure
- Docker
- Node.js

---

## 🚦 API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat` | POST | AI chat interface |
| `/api/v1/sky-events` | POST | Add sky events |
| `/api/v1/weather/alerts` | POST | Add weather alerts |
| `/api/v1/missions` | POST | Add mission data |
| `/api/v1/predictions` | POST | Add predictions |
| `/api/v1/earth-impact` | POST | Add Earth insights |
| `/api/v1/learning/content` | POST | Add learning material |
| `/api/v1/nasa` | GET | NASA data proxy |

Docs available at:  
➡️ `http://localhost:8000/docs`

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/spacescope.git
cd spacescope
```

### 2. Setup environment variables

Create `backend/.env`:

```env
DATABASE_URL=postgresql://spacescope_user:spacescope_password@postgres:5432/spacescope_db
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

### 3. Run the project

```bash
docker compose up --build
```

### 4. Access

| Service | URL |
|---------|------|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🧪 Testing

```bash
python test_endpoints_v2.py
```

---

## 🧩 Folder Structure

```
spacescope/
│
├── backend/
│   ├── app/
│   ├── tasks/
│   ├── models/
│   ├── main.py
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── pages/
│
├── docker-compose.yml
└── README.md
```

---

## 🏆 Accomplishments

- Designed a modular AI + data platform from scratch  
- Integrated live space data and generative AI  
- Built a scalable async backend architecture  
- Delivered a complete end-to-end system in hackathon time  

---

## 📈 What’s Next

- Live satellite feeds  
- Interactive sky maps  
- User accounts & personalization  
- Real-time alert notifications  
- Mobile app  
