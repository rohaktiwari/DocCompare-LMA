import re
from typing import List, Dict, Any

class RiskEngine:
    def __init__(self):
        self.standard_leverage = 3.00
        self.standard_interest_cover = 4.00
        self.standard_grace_period = 3

    def analyze_deal(self, deal_text: str, template_text: str) -> Dict[str, Any]:
        """
        Analyzes a deal text against a template and returns a risk report.
        """
        deviations = []
        
        # 1. Leverage Ratio Analysis
        lev_match = re.search(r"Leverage Ratio.*?not exceed\s+(\d+\.\d+):1", deal_text, re.IGNORECASE)
        if lev_match:
            lev_val = float(lev_match.group(1))
            if lev_val > 4.00:
                deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Leverage Ratio",
                    "risk_level": "High",
                    "description": f"Leverage Ratio cap is {lev_val}:1 (Standard: {self.standard_leverage}:1). Significantly looser than LMA standard.",
                    "recommendation": "Negotiate tighter cap or add margin ratchet."
                })
            elif lev_val > self.standard_leverage:
                deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Leverage Ratio",
                    "risk_level": "Medium",
                    "description": f"Leverage Ratio cap is {lev_val}:1 (Standard: {self.standard_leverage}:1). Slightly looser than market standard.",
                    "recommendation": "Monitor closely."
                })
            else:
                 deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Leverage Ratio",
                    "risk_level": "Low",
                    "description": f"Leverage Ratio matches LMA standard ({lev_val}:1).",
                    "recommendation": "None."
                })
        else:
             deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Leverage Ratio",
                    "risk_level": "High",
                    "description": "Leverage Ratio clause not found or format unrecognized.",
                    "recommendation": "Verify existence of financial covenants."
                })

        # 2. Interest Cover Analysis
        ic_match = re.search(r"Interest Cover.*?not be less than\s+(\d+\.\d+):1", deal_text, re.IGNORECASE)
        if ic_match:
            ic_val = float(ic_match.group(1))
            if ic_val < 2.50:
                deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Interest Cover",
                    "risk_level": "High",
                    "description": f"Interest Cover floor is {ic_val}:1 (Standard: {self.standard_interest_cover}:1). Very weak protection.",
                    "recommendation": "Request minimum 3.00:1 or 4.00:1."
                })
            elif ic_val < self.standard_interest_cover:
                deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Interest Cover",
                    "risk_level": "Medium",
                    "description": f"Interest Cover floor is {ic_val}:1 (Standard: {self.standard_interest_cover}:1). Below LMA standard.",
                    "recommendation": "Standard is usually 4.00:1."
                })
            else:
                deviations.append({
                    "clause": "Financial Covenants",
                    "type": "Interest Cover",
                    "risk_level": "Low",
                    "description": "Interest Cover matches or exceeds standard.",
                    "recommendation": "None."
                })

        # 3. Grace Period Analysis
        grace_match = re.search(r"payment is made within\s+(\d+)\s+Business Days", deal_text, re.IGNORECASE)
        if grace_match:
            grace_days = int(grace_match.group(1))
            if grace_days > 5:
                deviations.append({
                    "clause": "Events of Default",
                    "type": "Non-payment Grace Period",
                    "risk_level": "High",
                    "description": f"Grace period is {grace_days} days (Standard: {self.standard_grace_period} days). Excessive cure period.",
                    "recommendation": "Reduce to 3 business days for administrative errors only."
                })
            elif grace_days > self.standard_grace_period:
                deviations.append({
                    "clause": "Events of Default",
                    "type": "Non-payment Grace Period",
                    "risk_level": "Medium",
                    "description": f"Grace period is {grace_days} days (Standard: {self.standard_grace_period} days).",
                    "recommendation": "Standard is 3 days."
                })
        
        # 4. Cross Default Threshold
        cross_match = re.search(r"aggregate amount.*?exceeds EUR\s+([\d,]+)", deal_text, re.IGNORECASE)
        if cross_match:
            # Found a specific threshold, checking if it exists implies it might be higher than standard '0' or low amount
            threshold_str = cross_match.group(1).replace(",", "")
            threshold = float(threshold_str)
            if threshold > 2000000: # Arbitrary threshold for demo
                 deviations.append({
                    "clause": "Events of Default",
                    "type": "Cross Default Threshold",
                    "risk_level": "Medium",
                    "description": f"Cross default threshold is EUR {threshold:,.0f}. Higher than typical zero-floor standard.",
                    "recommendation": "Check group size to justify this threshold."
                })

        # Calculate Overall Score (Simple weighted sum)
        risk_weights = {"High": 5, "Medium": 2, "Low": 0}
        total_risk = sum(risk_weights.get(d["risk_level"], 0) for d in deviations)
        
        # Normalize to 0-10 scale (inverse: 0 is good, 10 is bad? Prompt says 0-10 risk score)
        # Let's say max possible risk in this simple model is ~15-20. 
        # We'll cap it at 10.
        overall_score = min(total_risk, 10)
        
        risk_label = "Low"
        if overall_score >= 7:
            risk_label = "High"
        elif overall_score >= 3:
            risk_label = "Medium"

        return {
            "overall_score": overall_score,
            "risk_label": risk_label,
            "deviations": deviations,
            "counts": {
                "High": len([d for d in deviations if d["risk_level"] == "High"]),
                "Medium": len([d for d in deviations if d["risk_level"] == "Medium"]),
                "Low": len([d for d in deviations if d["risk_level"] == "Low"]),
            }
        }

