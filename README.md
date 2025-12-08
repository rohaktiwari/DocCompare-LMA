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

# Optional: Add Anthropic API key for AI explanations
# The system works WITHOUT this - AI just enhances the UX
cp .env.example .env
# Edit .env and add your key if desired

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
1. **Single Deal**: Select "Deal_InvestmentGrade_Clean.txt" for a compliant deal, or "Deal_Distressed_Multiple_Waivers.txt" for a high-risk one.
2. **Analysis**: See deterministic risk scoring and clause extraction.
3. **Portfolio**: Add the analyzed deal to the portfolio and view the dashboard metrics.
4. **Amendments**: Track version changes.

## How It Works

**Core Intelligence (Works WITHOUT AI):**
- Proprietary LMA document parser extracts structured covenant data
- Rule-based risk scoring engine compares against market standards
- Deterministic risk quantification (e.g., 5.5x leverage = 7/10 risk score)
- Portfolio aggregation and outlier detection

**AI Enhancement Layer (Optional):**
- If ANTHROPIC_API_KEY is provided, generates plain-English explanations
- If no API key, uses template-based explanations
- AI explains OUR findings, doesn't do the analysis

**This is NOT an AI wrapper** - it's an intelligent document analysis tool with optional AI-enhanced UX.
