import re
from typing import List, Dict, Any, Optional
import os

class LMADocumentParser:
    """Extracts structured data from LMA-formatted loan documents"""
    
    def __init__(self):
        # LMA standard clause patterns
        # Updated regexes to be more robust for the provided sample deals
        self.clause_patterns = {
            'leverage_ratio': r'Leverage\s+Ratio.*?not\s+exceed(?:[:\s\w\-\n]*?)(\d+\.?\d*):1',
            'interest_cover': r'Interest\s+Cover.*?not\s+be\s+less\s+than\s+(\d+\.?\d*):1',
            'grace_period': r'payment\s+is\s+made\s+within\s+(\d+)\s+Business\s+Days',
            'cross_default': r'(?:aggregate\s+amount.*?exceeds?|exceeding)\s+(?:EUR|USD|GBP)\s+([\d,]+)',
            'negative_pledge': r'(Negative\s+Pledge.*?)(?=\n\n|\n\d+\.|\Z)',
            'disposals': r'(Disposals.*?)(?=\n\n|\n\d+\.|\Z)',
        }
    
    def extract_covenant(self, text: str, pattern_key: str) -> Optional[Dict[str, Any]]:
        """Extract a specific covenant and return structured data"""
        pattern = self.clause_patterns.get(pattern_key)
        if not pattern:
            return None
        
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if not match:
            return None
        
        return {
            'found': True,
            'value': match.group(1) if match.groups() else None,
            'full_text': match.group(0),
            'position': match.start()
        }
    
    def parse_document(self, doc_text: str) -> Dict[str, Any]:
        """Parse document into structured covenant data"""
        return {
            'leverage_ratio': self.extract_covenant(doc_text, 'leverage_ratio'),
            'interest_cover': self.extract_covenant(doc_text, 'interest_cover'),
            'grace_period': self.extract_covenant(doc_text, 'grace_period'),
            'cross_default': self.extract_covenant(doc_text, 'cross_default'),
            'negative_pledge': self.extract_covenant(doc_text, 'negative_pledge'),
            'disposals': self.extract_covenant(doc_text, 'disposals'),
        }

class RiskScoringEngine:
    """Deterministic, rule-based risk scoring - NO AI"""
    
    def __init__(self):
        # LMA market standards (calibrated to actual market practice)
        self.standards = {
            'leverage_ratio_investment_grade': 3.0,
            'leverage_ratio_leveraged': 4.0,
            'leverage_ratio_aggressive': 5.0,
            'interest_cover_standard': 4.0,
            'interest_cover_minimum': 3.0,
            'grace_period_standard': 3,
            'grace_period_max_acceptable': 5,
            'cross_default_threshold_standard': 0,  # Zero floor is standard
        }
    
    def score_leverage_ratio(self, extracted_value: float, deal_type: str = 'leveraged') -> Dict[str, Any]:
        """Score leverage covenant deviation"""
        standard = self.standards['leverage_ratio_leveraged']
        
        if extracted_value <= standard:
            risk_level = 'Low'
            risk_score = 0
            severity = 'Compliant with LMA standard'
        elif extracted_value <= 4.5:
            risk_level = 'Medium'
            risk_score = 4
            severity = 'Moderately looser than standard'
        elif extracted_value <= 5.5:
            risk_level = 'High'
            risk_score = 7
            severity = 'Significantly weaker protection'
        else:
            risk_level = 'High'
            risk_score = 9
            severity = 'Extremely weak covenant package'
        
        return {
            'clause_type': 'Leverage Ratio',
            'extracted_value': extracted_value,
            'standard_value': standard,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'severity': severity,
            'deviation_pct': ((extracted_value - standard) / standard * 100),
        }
    
    def score_interest_cover(self, extracted_value: float) -> Dict[str, Any]:
        """Score interest cover deviation"""
        standard = self.standards['interest_cover_standard']
        
        if extracted_value >= standard:
            risk_level = 'Low'
            risk_score = 0
            severity = 'Meets or exceeds standard'
        elif extracted_value >= 3.5:
            risk_level = 'Medium'
            risk_score = 3
            severity = 'Slightly below standard'
        elif extracted_value >= 2.5:
            risk_level = 'High'
            risk_score = 7
            severity = 'Weak debt service coverage'
        else:
            risk_level = 'High'
            risk_score = 9
            severity = 'Very weak protection - high default risk'
        
        return {
            'clause_type': 'Interest Cover',
            'extracted_value': extracted_value,
            'standard_value': standard,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'severity': severity,
            'deviation_pct': ((standard - extracted_value) / standard * 100),
        }
    
    def score_grace_period(self, extracted_days: int) -> Dict[str, Any]:
        """Score grace period deviation"""
        standard = self.standards['grace_period_standard']
        
        if extracted_days <= standard:
            risk_level = 'Low'
            risk_score = 0
            severity = 'Standard grace period'
        elif extracted_days <= 5:
            risk_level = 'Medium'
            risk_score = 3
            severity = 'Extended cure period'
        else:
            risk_level = 'High'
            risk_score = 6
            severity = 'Excessive cure period - reduces lender protection'
        
        return {
            'clause_type': 'Non-payment Grace Period',
            'extracted_value': extracted_days,
            'standard_value': standard,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'severity': severity,
            'deviation_days': extracted_days - standard,
        }
    
    def score_cross_default(self, threshold_value: float) -> Dict[str, Any]:
        """Score cross default threshold"""
        if threshold_value == 0:
            risk_level = 'Low'
            risk_score = 0
            severity = 'Zero-floor standard (most protective)'
        elif threshold_value <= 1_000_000:
            risk_level = 'Low'
            risk_score = 1
            severity = 'Low threshold - acceptable'
        elif threshold_value <= 5_000_000:
            risk_level = 'Medium'
            risk_score = 4
            severity = 'Material threshold - reduces cross-default protection'
        else:
            risk_level = 'High'
            risk_score = 7
            severity = 'Very high threshold - significant gap in lender protection'
        
        return {
            'clause_type': 'Cross Default Threshold',
            'extracted_value': threshold_value,
            'standard_value': 0,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'severity': severity,
        }

class AIExplanationEngine:
    """Optional AI layer for plain-English explanations"""
    
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.enabled = bool(self.api_key)
        if self.enabled:
            print("AI explanations enabled")
        else:
            print("AI explanations disabled - using fallback mode")
    
    def generate_explanation(self, risk_data: Dict[str, Any], template_context: str = '') -> str:
        """Generate plain-English explanation of risk finding"""
        
        if not self.enabled:
            # Fallback: template-based explanation if no API key
            return self._fallback_explanation(risk_data)
        
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.api_key)
            
            prompt = f"""You are a loan documentation expert. Provide a concise 2-3 sentence explanation for a credit committee.
**Deviation Found:**
- Clause: {risk_data['clause_type']}
- Current Value: {risk_data['extracted_value']}
- LMA Standard: {risk_data['standard_value']}
- Risk Level: {risk_data['risk_level']}
- Severity: {risk_data['severity']}

Explain: (1) What this means practically, (2) Why it matters for lender protection.
Keep it professional and fact-based. No preamble."""

            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"AI explanation failed: {e}")
            return self._fallback_explanation(risk_data)
    
    def _fallback_explanation(self, risk_data: Dict[str, Any]) -> str:
        """Deterministic fallback if AI unavailable"""
        clause = risk_data['clause_type']
        current = risk_data['extracted_value']
        standard = risk_data['standard_value']
        severity = risk_data['severity']
        
        return f"{clause} is set at {current} compared to the LMA standard of {standard}. {severity}. This impacts lender protection by allowing the borrower more flexibility before covenant breach."

class RiskEngine:
    """Main engine - combines parsing, scoring, and optional AI"""
    
    def __init__(self):
        self.parser = LMADocumentParser()
        self.scorer = RiskScoringEngine()
        self.ai_explainer = AIExplanationEngine()
    
    def analyze_deal(self, deal_text: str, template_text: str) -> Dict[str, Any]:
        """
        Full analysis pipeline:
        1. Parse both documents
        2. Compare structurally
        3. Score deviations
        4. Generate explanations
        """
        
        # Parse documents
        deal_data = self.parser.parse_document(deal_text)
        # template_data = self.parser.parse_document(template_text)
        
        deviations = []
        total_risk_score = 0
        
        # Analyze Leverage Ratio
        if deal_data['leverage_ratio'] and deal_data['leverage_ratio']['value']:
            lev_value = float(deal_data['leverage_ratio']['value'])
            risk_data = self.scorer.score_leverage_ratio(lev_value)
            
            description = self.ai_explainer.generate_explanation(risk_data)
            recommendation = self._generate_recommendation(risk_data)
            
            deviations.append({
                'clause': 'Financial Covenants',
                'type': 'Leverage Ratio',
                'risk_level': risk_data['risk_level'],
                'description': description,
                'recommendation': recommendation,
                'metadata': risk_data
            })
            
            total_risk_score += risk_data['risk_score']
        
        # Analyze Interest Cover
        if deal_data['interest_cover'] and deal_data['interest_cover']['value']:
            ic_value = float(deal_data['interest_cover']['value'])
            risk_data = self.scorer.score_interest_cover(ic_value)
            
            description = self.ai_explainer.generate_explanation(risk_data)
            recommendation = self._generate_recommendation(risk_data)
            
            deviations.append({
                'clause': 'Financial Covenants',
                'type': 'Interest Cover',
                'risk_level': risk_data['risk_level'],
                'description': description,
                'recommendation': recommendation,
                'metadata': risk_data
            })
            
            total_risk_score += risk_data['risk_score']
        
        # Analyze Grace Period
        if deal_data['grace_period'] and deal_data['grace_period']['value']:
            grace_days = int(deal_data['grace_period']['value'])
            risk_data = self.scorer.score_grace_period(grace_days)
            
            description = self.ai_explainer.generate_explanation(risk_data)
            recommendation = self._generate_recommendation(risk_data)
            
            deviations.append({
                'clause': 'Events of Default',
                'type': 'Non-payment Grace Period',
                'risk_level': risk_data['risk_level'],
                'description': description,
                'recommendation': recommendation,
                'metadata': risk_data
            })
            
            total_risk_score += risk_data['risk_score']
        
        # Analyze Cross Default
        if deal_data['cross_default'] and deal_data['cross_default']['value']:
            threshold_str = deal_data['cross_default']['value'].replace(',', '')
            threshold = float(threshold_str)
            risk_data = self.scorer.score_cross_default(threshold)
            
            description = self.ai_explainer.generate_explanation(risk_data)
            recommendation = self._generate_recommendation(risk_data)
            
            deviations.append({
                'clause': 'Events of Default',
                'type': 'Cross Default Threshold',
                'risk_level': risk_data['risk_level'],
                'description': description,
                'recommendation': recommendation,
                'metadata': risk_data
            })
            
            total_risk_score += risk_data['risk_score']
        
        # Calculate overall metrics
        overall_score = min(total_risk_score, 10)
        
        risk_label = 'Low'
        if overall_score >= 7:
            risk_label = 'High'
        elif overall_score >= 3:
            risk_label = 'Medium'
        
        return {
            'overall_score': overall_score,
            'risk_label': risk_label,
            'deviations': deviations,
            'counts': {
                'High': len([d for d in deviations if d['risk_level'] == 'High']),
                'Medium': len([d for d in deviations if d['risk_level'] == 'Medium']),
                'Low': len([d for d in deviations if d['risk_level'] == 'Low']),
            },
            'ai_enabled': self.ai_explainer.enabled
        }
    
    def _generate_recommendation(self, risk_data: Dict[str, Any]) -> str:
        """Generate actionable recommendation"""
        risk_level = risk_data['risk_level']
        clause = risk_data['clause_type']
        
        if risk_level == 'High':
            if 'Leverage' in clause:
                return "Negotiate tighter covenant or add margin ratchet. Consider quarterly testing."
            elif 'Interest Cover' in clause:
                return "Request minimum 3.5:1 or add EBITDA adjustments to improve coverage."
            elif 'Grace Period' in clause:
                return "Reduce to 3 business days. Current period weakens default protection."
            elif 'Cross Default' in clause:
                return "Lower threshold or remove minimum. Current threshold creates protection gap."
        elif risk_level == 'Medium':
            return f"Monitor closely. Consider tightening in next amendment or for future similar deals."
        else:
            return "Acceptable. Complies with LMA market standard."
        
        return "Review with credit committee."
