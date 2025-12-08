from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import datetime

router = APIRouter()

@router.get("/{deal_id}", response_class=PlainTextResponse)
def get_report(deal_id: str):
    # Generate a simple text report
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""
==================================================
LMA COMPLIANCE REPORT - DO NOT DISTRIBUTE
==================================================
Deal Ref: {deal_id}
Date: {timestamp}
Status: REQUIRES APPROVAL

EXECUTIVE SUMMARY
-----------------
This facility agreement contains material deviations from the LMA standard.
Risk Score: HIGH

KEY RISKS IDENTIFIED
--------------------
1. Financial Covenants: Leverage Ratio exceeds standard (4.50:1 vs 3.00:1).
2. Interest Cover: Floor is lower than market standard.
3. Events of Default: Grace periods exceed 3 business days.

RECOMMENDATION
--------------
Refer to Credit Committee for Level 2 Approval.
    """
    return report
