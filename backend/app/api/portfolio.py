from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import random

router = APIRouter()

class PortfolioItem(BaseModel):
    id: str
    deal_name: str
    jurisdiction: str
    vintage: str
    risk_score: float
    risk_label: str
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    is_red_flag: bool

@router.get("/", response_model=List[PortfolioItem])
def get_portfolio():
    # Generate deterministic dummy data for the demo
    deals = [
        {"name": "Project Alpha", "jur": "English Law", "yr": "2023", "score": 2, "h": 0, "m": 2},
        {"name": "Project Beta", "jur": "English Law", "yr": "2023", "score": 8, "h": 3, "m": 1},
        {"name": "Project Gamma", "jur": "Irish Law", "yr": "2018", "score": 9, "h": 4, "m": 2},
        {"name": "Acme Corp Refi", "jur": "English Law", "yr": "2021", "score": 4, "h": 1, "m": 3},
        {"name": "BlueSky Holdings", "jur": "Luxembourg", "yr": "2022", "score": 1, "h": 0, "m": 0},
        {"name": "Orion Energy", "jur": "UAE", "yr": "2019", "score": 7, "h": 2, "m": 4},
        {"name": "Titan Infrastructure", "jur": "English Law", "yr": "2020", "score": 3, "h": 0, "m": 3},
        {"name": "Zenith Telecom", "jur": "Irish Law", "yr": "2023", "score": 2, "h": 0, "m": 1},
        {"name": "Apex Logistics", "jur": "English Law", "yr": "2016", "score": 8, "h": 3, "m": 2},
        {"name": "Nova Retail", "jur": "English Law", "yr": "2022", "score": 0, "h": 0, "m": 0},
        {"name": "Echo Media", "jur": "French Law", "yr": "2021", "score": 5, "h": 1, "m": 2},
        {"name": "Sierra Mining", "jur": "English Law", "yr": "2019", "score": 6, "h": 2, "m": 1},
    ]

    portfolio = []
    for i, d in enumerate(deals):
        risk_label = "Low"
        if d["score"] >= 7: risk_label = "High"
        elif d["score"] >= 3: risk_label = "Medium"
        
        is_red_flag = d["score"] >= 7 or d["h"] >= 2 or (int(d["yr"]) < 2020 and d["score"] > 4)

        portfolio.append({
            "id": str(i + 1),
            "deal_name": d["name"],
            "jurisdiction": d["jur"],
            "vintage": d["yr"],
            "risk_score": float(d["score"]),
            "risk_label": risk_label,
            "high_risk_count": d["h"],
            "medium_risk_count": d["m"],
            "low_risk_count": (len(d["name"]) % 5) + 1,
            "is_red_flag": is_red_flag
        })
    
    return portfolio

