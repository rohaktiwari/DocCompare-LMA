from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze, portfolio, report, amendments

app = FastAPI(title="DocCompare LMA", version="1.0.0")

# Allow CORS for frontend
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(report.router, prefix="/api/report", tags=["Report"])
app.include_router(amendments.router, prefix="/api/amendments", tags=["Amendments"])

@app.get("/")
def read_root():
    return {"message": "DocCompare LMA API is running"}

