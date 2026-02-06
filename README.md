# Digital Footprint Analyzer

A "Cyber/Hacker" themed OSINT tool to analyze digital footprints.

## Features
- **Deep Dive Search**: Aggregates data from Google, Social Media (LinkedIn, Instagram), and more.
- **Premium UI**: Matrix-style interface with glassmorphism and animations.
- **Privacy Focused**: Uses only public data (OSINT).

## Setup

### Backend
1. Navigate to `backend/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn main:app --reload`
   - Access API at: `http://localhost:8000`

### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Start app: `npm run dev`
   - Access UI at: `http://localhost:5173`

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS, Framer Motion
- **Backend**: Python, FastAPI, GoogleSearch
