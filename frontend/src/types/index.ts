export interface Deviation {
  clause: string;
  type: string;
  risk_level: 'High' | 'Medium' | 'Low';
  description: string;
  recommendation: string;
}

export interface AnalysisResult {
  deal_name: string;
  template_name: string;
  overall_score: number;
  risk_label: 'High' | 'Medium' | 'Low';
  deviations: Deviation[];
  counts: {
    High: number;
    Medium: number;
    Low: number;
  };
}

export interface PortfolioItem {
  id: string;
  deal_name: string;
  jurisdiction: string;
  vintage: string;
  risk_score: number;
  risk_label: 'High' | 'Medium' | 'Low';
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  is_red_flag: boolean;
}

