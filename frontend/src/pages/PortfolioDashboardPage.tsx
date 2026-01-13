import React, { useEffect, useState } from 'react';
import { getPortfolio } from '../api/client';
import { PortfolioItem } from '../types';
import { Filter, ArrowUpDown, AlertCircle, FileText, Globe, Calendar } from 'lucide-react';

type RiskLevel = 'High' | 'Medium' | 'Low';
const RiskPill = ({ level }: { level: RiskLevel }) => {
  const colors: Record<RiskLevel, string> = {
    High: 'bg-red-100 text-red-700',
    Medium: 'bg-amber-100 text-amber-700',
    Low: 'bg-emerald-100 text-emerald-700',
  };
  return <span className={`px-2 py-0.5 rounded text-xs font-semibold ${colors[level]}`}>{level}</span>;
};

const PortfolioDashboardPage = () => {
  const [data, setData] = useState<PortfolioItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterJur, setFilterJur] = useState('All');

  useEffect(() => {
    getPortfolio().then(d => {
      setData(d);
      setLoading(false);
    });
  }, []);

  const filteredData = filterJur === 'All' 
    ? data 
    : data.filter(d => d.jurisdiction === filterJur);

  // Calculate stats
  const totalDeals = data.length;
  const highRiskDeals = data.filter(d => d.risk_label === 'High').length;
  const avgScore = (data.reduce((acc, curr) => acc + curr.risk_score, 0) / totalDeals).toFixed(1);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
           <h1 className="text-2xl font-bold text-slate-900">Portfolio Compliance</h1>
           <p className="text-slate-500">Monitor documentation risk across your loan book.</p>
        </div>
        <button className="bg-white border border-slate-300 text-slate-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-slate-50">
           Export Report
        </button>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
         <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
           <div>
             <div className="text-sm font-medium text-slate-500">Total Deals</div>
             <div className="text-2xl font-bold text-slate-900">{totalDeals}</div>
           </div>
           <div className="h-10 w-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500">
             <FileText size={20} />
           </div>
         </div>
         <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
           <div>
             <div className="text-sm font-medium text-slate-500">High Risk Exposure</div>
             <div className="text-2xl font-bold text-red-600">{highRiskDeals}</div>
           </div>
           <div className="h-10 w-10 bg-red-50 rounded-full flex items-center justify-center text-red-500">
             <AlertCircle size={20} />
           </div>
         </div>
         <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
           <div>
             <div className="text-sm font-medium text-slate-500">Avg Risk Score</div>
             <div className="text-2xl font-bold text-slate-900">{avgScore}</div>
           </div>
           <div className="h-10 w-10 bg-brand-50 rounded-full flex items-center justify-center text-brand-600">
             <ActivityIcon />
           </div>
         </div>
      </div>

      {/* Main Table */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
        {/* Toolbar */}
        <div className="px-6 py-4 border-b border-slate-200 flex flex-wrap items-center gap-4">
          <div className="flex items-center space-x-2 text-sm text-slate-600">
            <Filter size={16} />
            <span className="font-medium">Filter by Jurisdiction:</span>
            <select 
              value={filterJur} 
              onChange={(e) => setFilterJur(e.target.value)}
              className="border-none bg-slate-100 rounded-md py-1 pl-2 pr-8 text-sm focus:ring-0"
            >
              <option value="All">All Jurisdictions</option>
              <option value="English Law">English Law</option>
              <option value="Irish Law">Irish Law</option>
              <option value="Luxembourg">Luxembourg</option>
              <option value="UAE">UAE</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider cursor-pointer hover:text-slate-700">
                  <div className="flex items-center space-x-1">
                    <span>Deal Name</span>
                  </div>
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Jurisdiction
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Vintage
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                   Risk Score
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                   Deviations (H/M/L)
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                   Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                    Loading portfolio data...
                  </td>
                </tr>
              ) : filteredData.map((item) => (
                <tr key={item.id} className={`hover:bg-slate-50 transition-colors ${item.is_red_flag ? 'bg-red-50/30' : ''}`}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                       {item.is_red_flag && <AlertCircle size={16} className="text-red-500 mr-2" />}
                       <span className={`font-medium ${item.is_red_flag ? 'text-red-900' : 'text-slate-900'}`}>{item.deal_name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                    <div className="flex items-center space-x-1">
                      <Globe size={14} className="text-slate-400" />
                      <span>{item.jurisdiction}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                    <div className="flex items-center space-x-1">
                       <Calendar size={14} className="text-slate-400" />
                       <span>{item.vintage}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                     <div className="flex items-center space-x-2">
                        <span className={`font-bold ${
                           item.risk_score >= 7 ? 'text-red-600' : 
                           item.risk_score >= 4 ? 'text-amber-600' : 'text-slate-600'
                        }`}>{item.risk_score}</span>
                        <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                           <div 
                              className={`h-full rounded-full ${
                                 item.risk_score >= 7 ? 'bg-red-500' : 
                                 item.risk_score >= 4 ? 'bg-amber-500' : 'bg-emerald-500'
                              }`} 
                              style={{ width: `${item.risk_score * 10}%` }} 
                           />
                        </div>
                     </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                     <div className="flex space-x-1">
                        <span className="px-1.5 bg-red-100 text-red-700 rounded text-xs font-bold">{item.high_risk_count}</span>
                        <span className="px-1.5 bg-amber-100 text-amber-700 rounded text-xs font-bold">{item.medium_risk_count}</span>
                        <span className="px-1.5 bg-emerald-100 text-emerald-700 rounded text-xs font-bold">{item.low_risk_count}</span>
                     </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <RiskPill level={item.risk_label} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const ActivityIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
  </svg>
);

export default PortfolioDashboardPage;

