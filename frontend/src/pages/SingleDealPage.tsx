import React, { useState, useEffect } from 'react';
import { Upload, FileText, AlertTriangle, CheckCircle, ArrowRight, Activity, ChevronRight, X } from 'lucide-react';
import { analyzeDeal, getSamples, api, getReportUrl } from '../api/client';
import { AnalysisResult, Deviation } from '../types';

const RiskBadge = ({ level }: { level: 'High' | 'Medium' | 'Low' }) => {
  const colors = {
    High: 'bg-red-100 text-red-700 border-red-200',
    Medium: 'bg-amber-100 text-amber-700 border-amber-200',
    Low: 'bg-emerald-100 text-emerald-700 border-emerald-200',
  };
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${colors[level]}`}>
      {level.toUpperCase()}
    </span>
  );
};

const SingleDealPage = () => {
  const [samples, setSamples] = useState<string[]>([]);
  const [selectedSample, setSelectedSample] = useState<string>('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [selectedDeviation, setSelectedDeviation] = useState<Deviation | null>(null);

  useEffect(() => {
    getSamples().then(setSamples);
  }, []);

  const handleAnalyze = async () => {
    if (!selectedSample) return;
    setAnalyzing(true);
    setResult(null);
    try {
      // Artificial delay for effect
      await new Promise(resolve => setTimeout(resolve, 800));
      const data = await analyzeDeal(selectedSample);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Introduction */}
      {!result && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center max-w-2xl mx-auto mt-12">
          <div className="bg-brand-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
            <Upload className="text-brand-600" size={32} />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">Upload Facility Agreement</h1>
          <p className="text-slate-500 mb-8">
            Compare your deal against the LMA Leveraged Facility Agreement (2023) standard template.
          </p>
          
          <div className="max-w-md mx-auto space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1 text-left">Select a sample document</label>
              <select 
                className="w-full rounded-md border-slate-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 py-2 px-3 border"
                value={selectedSample}
                onChange={(e) => setSelectedSample(e.target.value)}
              >
                <option value="">-- Select a file --</option>
                {samples.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
            
            <button 
              onClick={handleAnalyze}
              disabled={!selectedSample || analyzing}
              className={`w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-md text-white font-medium transition-all ${
                !selectedSample || analyzing 
                  ? 'bg-slate-300 cursor-not-allowed' 
                  : 'bg-brand-600 hover:bg-brand-700 shadow-md hover:shadow-lg'
              }`}
            >
              {analyzing ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <FileText size={20} />
                  <span>Analyze Document</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Results Dashboard */}
      {result && (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-6">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-2xl font-bold text-slate-900">{result.deal_name}</h2>
              <p className="text-slate-500 text-sm">Compared against: <span className="font-medium text-slate-700">{result.template_name}</span></p>
            </div>
            <div className="flex items-center space-x-3">
               <button 
                onClick={() => setResult(null)}
                className="text-slate-500 hover:text-slate-700 text-sm font-medium"
               >
                 Analyze Another
               </button>
               <a 
                 href={getReportUrl(result.deal_name)}
                 target="_blank"
                 rel="noreferrer"
                 className="bg-white border border-slate-300 text-slate-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-slate-50 flex items-center"
               >
                 Download Report
               </a>
            </div>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
              <div className="text-sm font-medium text-slate-500 mb-1">Overall Risk Score</div>
              <div className="flex items-baseline space-x-2">
                <span className={`text-3xl font-bold ${
                  result.risk_label === 'High' ? 'text-red-600' :
                  result.risk_label === 'Medium' ? 'text-amber-600' : 'text-emerald-600'
                }`}>{result.overall_score}/10</span>
                <RiskBadge level={result.risk_label} />
              </div>
            </div>
            
            <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-1">
                 <div className="text-sm font-medium text-slate-500">High Risk Deviations</div>
                 <AlertTriangle size={16} className="text-red-500" />
              </div>
              <div className="text-2xl font-bold text-slate-900">{result.counts.High}</div>
            </div>

            <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
               <div className="flex items-center justify-between mb-1">
                 <div className="text-sm font-medium text-slate-500">Medium Risk Deviations</div>
                 <Activity size={16} className="text-amber-500" />
              </div>
              <div className="text-2xl font-bold text-slate-900">{result.counts.Medium}</div>
            </div>

            <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
               <div className="flex items-center justify-between mb-1">
                 <div className="text-sm font-medium text-slate-500">Low Risk Items</div>
                 <CheckCircle size={16} className="text-emerald-500" />
              </div>
              <div className="text-2xl font-bold text-slate-900">{result.counts.Low}</div>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div>
                <div className="font-medium text-blue-900">Add to Portfolio</div>
                <div className="text-sm text-blue-700">Track this deal in your portfolio dashboard</div>
              </div>
            </div>
            <button 
              onClick={async () => {
                try {
                  await api.post('/analyze/add-to-portfolio', {
                    sample_deal_id: selectedSample,
                    template_id: "LMA_Leveraged_2023.txt"
                  });
                  alert('Added to portfolio successfully!');
                } catch (err) {
                  console.error(err);
                  alert('Failed to add to portfolio');
                }
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
            >
              Add to Portfolio
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Deviations List */}
            <div className="lg:col-span-2 bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
                <h3 className="font-semibold text-slate-900">Detected Deviations</h3>
                <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">{result.deviations.length} items found</span>
              </div>
              <div className="divide-y divide-slate-100">
                {result.deviations.map((d, idx) => (
                  <div 
                    key={idx}
                    onClick={() => setSelectedDeviation(d)}
                    className={`px-6 py-4 cursor-pointer transition-colors hover:bg-slate-50 group ${
                      selectedDeviation === d ? 'bg-brand-50 hover:bg-brand-50' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                           <RiskBadge level={d.risk_level} />
                           <span className="text-sm font-medium text-slate-900">{d.type}</span>
                           <span className="text-xs text-slate-400">• {d.clause}</span>
                        </div>
                        <p className="text-sm text-slate-600 line-clamp-1">{d.description}</p>
                      </div>
                      <ChevronRight size={18} className={`text-slate-300 group-hover:text-slate-400 ${
                         selectedDeviation === d ? 'text-brand-400' : ''
                      }`} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Detail View (Sticky) */}
            <div className="lg:col-span-1">
              {selectedDeviation ? (
                <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-6 sticky top-24">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-slate-900">Deviation Analysis</h3>
                    <button onClick={() => setSelectedDeviation(null)} className="text-slate-400 hover:text-slate-600">
                      <X size={18} />
                    </button>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                       <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Risk Level</span>
                       <div className="mt-1">
                          <RiskBadge level={selectedDeviation.risk_level} />
                       </div>
                    </div>

                    <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
                       <h4 className="text-xs font-semibold text-slate-500 uppercase mb-2">Description</h4>
                       <p className="text-sm text-slate-800">{selectedDeviation.description}</p>
                    </div>

                    <div className="p-3 bg-brand-50 rounded-md border border-brand-100">
                       <h4 className="text-xs font-semibold text-brand-700 uppercase mb-2 flex items-center">
                         <Activity size={12} className="mr-1" />
                         Recommendation
                       </h4>
                       <p className="text-sm text-brand-900">{selectedDeviation.recommendation}</p>
                    </div>

                     <div>
                       <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Source Clause</span>
                       <p className="text-xs text-slate-400 mt-1">{selectedDeviation.clause}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-slate-50 rounded-lg border border-slate-200 border-dashed p-8 text-center h-full flex flex-col items-center justify-center text-slate-400">
                   <FileText size={48} className="mb-4 opacity-50" />
                   <p className="text-sm font-medium">Select a deviation to see details</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SingleDealPage;

