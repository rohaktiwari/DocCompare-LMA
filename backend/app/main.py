from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze, portfolio, report, amendments

app = FastAPI(title="DocCompare LMA", version="1.0.0")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(report.router, prefix="/api/report", tags=["Report"])
app.include_router(amendments.router, prefix="/api/amendments", tags=["Amendments"])

@app.get("/")
def read_root():
    return {"message": "DocCompare LMA API is running"}

