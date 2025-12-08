# DocCompare LMA

LMA Standards Compliance Assistant - Hackathon Edition.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Tailwind (Vite)
- **Data**: Local file-based storage for demo simplicity.

## Setup & Run

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API will run at `http://localhost:8000`.
Docs at `http://localhost:8000/docs`.

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
App will run at `http://localhost:5173`.

## Demo Flow
1. **Single Deal**: Select "Deal_Beta_Risky.txt" to see Red/High Risk flags.
2. **Portfolio**: Shows dashboard of 10+ deals. Sort by "Risk Score".
3. **Amendments**: Select "Deal_Delta" versions to see timeline and redline.

