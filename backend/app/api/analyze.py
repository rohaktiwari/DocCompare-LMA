from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional, Any
import os
from app.core.risk_engine import RiskEngine

router = APIRouter()
risk_engine = RiskEngine()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class AnalysisRequest(BaseModel):
    deal_text: Optional[str] = None
    sample_deal_id: Optional[str] = None
    template_id: str = "LMA_Leveraged_2023.txt"

class Deviation(BaseModel):
    clause: str
    type: str
    risk_level: str
    description: str
    recommendation: str
    metadata: Optional[dict] = None

class AnalysisResult(BaseModel):
    deal_name: str
    template_name: str
    overall_score: float
    risk_label: str
    deviations: List[Deviation]
    counts: dict

@router.get("/samples")
def get_sample_deals():
    """Returns list of available sample deals for the demo."""
    samples_dir = os.path.join(DATA_DIR, "sample_deals")
    if not os.path.exists(samples_dir):
        return {"samples": []}
    files = [f for f in os.listdir(samples_dir) if f.endswith(".txt")]
    return {"samples": files}

@router.post("/", response_model=AnalysisResult)
async def analyze_deal(request: AnalysisRequest):
    # Load Template
    template_path = os.path.join(DATA_DIR, "templates", request.template_id)
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    
    with open(template_path, "r") as f:
        template_text = f.read()

    # Load Deal Text
    deal_text = ""
    deal_name = "Uploaded Document"

    if request.sample_deal_id:
        deal_path = os.path.join(DATA_DIR, "sample_deals", request.sample_deal_id)
        if not os.path.exists(deal_path):
            raise HTTPException(status_code=404, detail="Sample deal not found")
        with open(deal_path, "r") as f:
            deal_text = f.read()
        deal_name = request.sample_deal_id.replace(".txt", "").replace("_", " ")
    elif request.deal_text:
        deal_text = request.deal_text
    else:
        raise HTTPException(status_code=400, detail="No deal text provided")

    # Analyze
    result = risk_engine.analyze_deal(deal_text, template_text)
    
    return {
        "deal_name": deal_name,
        "template_name": request.template_id.replace(".txt", "").replace("_", " "),
        "overall_score": result["overall_score"],
        "risk_label": result["risk_label"],
        "deviations": result["deviations"],
        "counts": result["counts"]
    }

@router.post("/add-to-portfolio")
async def add_analysis_to_portfolio(request: AnalysisRequest):
    """Analyze a deal AND add it to portfolio"""
    
    # Run analysis (reuse existing logic)
    result = await analyze_deal(request)
    
    # Add to portfolio
    from app.api.portfolio import add_to_portfolio
    portfolio_result = add_to_portfolio(result)
    
    return {
        "analysis": result,
        "portfolio_status": portfolio_result
    }
