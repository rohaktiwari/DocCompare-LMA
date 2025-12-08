# DocCompare LMA - LMA Standards Compliance Assistant

## Problem Statement

Reviewing syndicated loan facility agreements is a high-friction, manual process. Syndication desks and credit risk teams spend 30-40 hours per deal manually cross-referencing hundreds of pages against LMA (Loan Market Association) standards. This creates bottlenecks in deal execution, increases legal spend, and leaves banks vulnerable to "covenant creep" where non-standard terms slip into portfolios unnoticed.

## Solution

DocCompare LMA is a compliance assistant that automates the review of facility agreements against market standards. Unlike generic contract analysis tools, it is purpose-built for the LMA framework. It parses key financial covenants, benchmarks them against risk thresholds, and aggregates findings into a portfolio-level view—reducing initial review time from hours to minutes.

## Key Features

- **Automated Deviation Analysis**: Instantly flags terms that deviate from LMA standards (e.g., Leverage Ratio > 4.5x, Grace Periods > 3 days).
- **Portfolio Risk Dashboard**: Aggregates risk across 20+ active deals, allowing teams to spot jurisdiction-specific trends (e.g., "Why are our Irish Law deals consistently weaker on Events of Default?").
- **Amendment Timeline Tracking**: Visualizes how terms evolve over time, highlighting where protections have been waived or loosened in subsequent amendments.
- **Credit Committee Reporting**: Generates exportable, standardized risk summaries to support faster credit decisions.

## Technical Approach

We employ a **hybrid intelligence model** to ensure accuracy and explainability:
1.  **Deterministic Core**: Critical risk scoring is handled by a rule-based engine, not a "black box" LLM. This ensures 100% consistency and auditability for compliance.
2.  **AI Enhancement Layer**: Generative AI is used strictly for explaining findings in plain English and summarizing context, providing the "why" behind the risk score.

## Demo Highlights

- **Single Deal Analysis**: Uploading a "Leveraged Aggressive" deal and instantly seeing a 7/10 High Risk score.
- **Drill-Down**: Clicking into a specific "Financial Covenant" deviation to see the extracted value (5.50x) vs. the LMA Standard (4.00x).
- **Portfolio View**: Identifying a "Red Flag" deal in the portfolio that combines an older vintage (2019) with high risk scores.
- **Amendment Tracking**: Comparing an Original Facility vs. Amendment 2 to see how the "Cross Default" threshold increased from €5M to €20M.

## Current Scope & Roadmap

**Prototype Coverage (Current):**
- Analyzes 4 critical covenant categories: Leverage Ratio, Interest Cover, Grace Periods, and Cross Default thresholds.
- Supports text-based facility agreements.
- Benchmarks against LMA Leveraged Facility standards.

**Production Roadmap (Next Steps):**
- **Expand Clause Library**: Scale from 4 to 20+ standard LMA clauses (Negative Pledge, Change of Control, Transferability).
- **Format Support**: Integrate OCR pipeline for scanned PDF support.
- **Custom Templates**: Allow banks to upload their own "House Standards" for comparison.
- **Entity Recognition**: Replace regex-based parsing with Named Entity Recognition (NER) for robust handling of varied formatting.

## Business Value

- **Efficiency**: Reduces initial document review time by an estimated **60%** (2-3 hours → 45 minutes).
- **Risk Mitigation**: Systematically catches high-risk deviations (e.g., excessive grace periods) that manual review might miss during crunch time.
- **Portfolio Insight**: Provides a "God's Eye View" of documentation risk, enabling proactive portfolio management rather than reactive firefighting.
- **Audit Trail**: Creates a consistent, digital record of compliance checks for every deal.

## Why This Approach?

In financial compliance, **consistency is king**. Pure LLM approaches can hallucinate or vary their scoring between runs. Our approach uses:
- **Regex-based pattern matching** for data extraction (fast, deterministic).
- **Rule-based scoring** for risk assessment (auditable, consistent).
- **LLMs** only for the final mile of explanation.
This ensures that if a covenant is 5.50x today, it will be flagged as "High Risk" tomorrow—every single time.

## Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, TypeScript, Tailwind CSS
- **Deployment**: Lightweight containerized architecture (Docker-ready) suitable for on-premise bank deployment.
