from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import json
import os
from pathlib import Path

router = APIRouter()

# Simple file-based storage for demo
PORTFOLIO_FILE = Path(__file__).parent.parent / "data" / "portfolio.json"

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
    analyzed_at: str

def load_portfolio() -> List[dict]:
    """Load portfolio from file"""
    if not PORTFOLIO_FILE.exists():
        # Initialize with some baseline deals
        return _get_initial_portfolio()
    
    with open(PORTFOLIO_FILE, 'r') as f:
        return json.load(f)

def save_portfolio(portfolio: List[dict]):
    """Save portfolio to file"""
    PORTFOLIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2)

def _get_initial_portfolio() -> List[dict]:
    """Initial portfolio with realistic baseline"""
    return [
        {
            "id": "1",
            "deal_name": "Project Alpha Term Loan",
            "jurisdiction": "English Law",
            "vintage": "2023",
            "risk_score": 2.0,
            "risk_label": "Low",
            "high_risk_count": 0,
            "medium_risk_count": 2,
            "low_risk_count": 3,
            "is_red_flag": False,
            "analyzed_at": "2024-11-15"
        },
        {
            "id": "2",
            "deal_name": "Acme Corp RCF",
            "jurisdiction": "English Law",
            "vintage": "2022",
            "risk_score": 4.0,
            "risk_label": "Medium",
            "high_risk_count": 1,
            "medium_risk_count": 3,
            "low_risk_count": 2,
            "is_red_flag": False,
            "analyzed_at": "2024-10-20"
        },
        {
            "id": "3",
            "deal_name": "Zenith Acquisition Facility",
            "jurisdiction": "Irish Law",
            "vintage": "2019",
            "risk_score": 8.0,
            "risk_label": "High",
            "high_risk_count": 3,
            "medium_risk_count": 2,
            "low_risk_count": 1,
            "is_red_flag": True,
            "analyzed_at": "2024-09-12"
        },
        {
            "id": "4",
            "deal_name": "BlueSky Holdings Bridge",
            "jurisdiction": "Luxembourg",
            "vintage": "2023",
            "risk_score": 1.0,
            "risk_label": "Low",
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 4,
            "is_red_flag": False,
            "analyzed_at": "2024-12-01"
        },
        {
            "id": "5",
            "deal_name": "Orion Energy Term Loan B",
            "jurisdiction": "UAE",
            "vintage": "2020",
            "risk_score": 7.0,
            "risk_label": "High",
            "high_risk_count": 2,
            "medium_risk_count": 4,
            "low_risk_count": 0,
            "is_red_flag": True,
            "analyzed_at": "2024-08-30"
        }
    ]

@router.get("/", response_model=List[PortfolioItem])
def get_portfolio():
    """Get all portfolio deals"""
    portfolio = load_portfolio()
    return portfolio

@router.post("/add")
def add_to_portfolio(analysis_result: dict):
    """Add a newly analyzed deal to the portfolio"""
    import datetime
    
    portfolio = load_portfolio()
    
    # Generate new ID
    new_id = str(max([int(p['id']) for p in portfolio] + [0]) + 1)
    
    # Determine if this is a red flag
    is_red_flag = (
        analysis_result['overall_score'] >= 7 or
        analysis_result['counts']['High'] >= 2
    )
    
    new_item = {
        "id": new_id,
        "deal_name": analysis_result['deal_name'],
        "jurisdiction": "English Law",  # TODO: Extract from document
        "vintage": str(datetime.datetime.now().year),
        "risk_score": analysis_result['overall_score'],
        "risk_label": analysis_result['risk_label'],
        "high_risk_count": analysis_result['counts']['High'],
        "medium_risk_count": analysis_result['counts']['Medium'],
        "low_risk_count": analysis_result['counts']['Low'],
        "is_red_flag": is_red_flag,
        "analyzed_at": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    portfolio.append(new_item)
    save_portfolio(portfolio)
    
    return {"message": "Added to portfolio", "item": new_item}

@router.get("/stats")
def get_portfolio_stats():
    """Get aggregated portfolio statistics"""
    portfolio = load_portfolio()
    
    if not portfolio:
        return {"error": "No portfolio data"}
    
    total_deals = len(portfolio)
    high_risk_deals = len([p for p in portfolio if p['risk_label'] == 'High'])
    avg_score = sum(p['risk_score'] for p in portfolio) / total_deals
    
    # Jurisdiction breakdown
    jurisdiction_breakdown = {}
    for p in portfolio:
        jur = p['jurisdiction']
        jurisdiction_breakdown[jur] = jurisdiction_breakdown.get(jur, 0) + 1
    
    # Vintage analysis
    old_docs = len([p for p in portfolio if int(p['vintage']) < 2020])
    
    return {
        "total_deals": total_deals,
        "high_risk_count": high_risk_deals,
        "high_risk_percentage": round(high_risk_deals / total_deals * 100, 1) if total_deals > 0 else 0,
        "average_risk_score": round(avg_score, 2) if total_deals > 0 else 0,
        "jurisdiction_breakdown": jurisdiction_breakdown,
        "pre_2020_documentation": old_docs,
        "red_flags": len([p for p in portfolio if p['is_red_flag']])
    }
