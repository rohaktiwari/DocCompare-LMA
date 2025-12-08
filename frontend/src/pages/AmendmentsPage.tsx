import React, { useState, useEffect } from 'react';
import { getVersions, compareVersions } from '../api/client';
import { GitCommit, ArrowRight, Clock, FileDiff } from 'lucide-react';

const AmendmentsPage = () => {
  const [baseDeal, setBaseDeal] = useState('Deal_Delta');
  const [versions, setVersions] = useState<string[]>([]);
  const [v1, setV1] = useState('');
  const [v2, setV2] = useState('');
  const [diff, setDiff] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load versions for the demo deal
    getVersions(baseDeal).then(vs => {
      setVersions(vs);
      if (vs.length >= 1) setV1(vs[0]);
      if (vs.length >= 2) setV2(vs[1]);
    });
  }, [baseDeal]);

  useEffect(() => {
    if (v1 && v2) {
      setLoading(true);
      compareVersions(v1, v2).then(d => {
        setDiff(d);
        setLoading(false);
      });
    }
  }, [v1, v2]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Amendment Tracking</h1>
        <p className="text-slate-500">Track evolution of terms across facility versions.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-4 mb-6">
           <div className="flex-1">
             <label className="block text-sm font-medium text-slate-700 mb-1">Base Version</label>
             <select 
               value={v1} 
               onChange={(e) => setV1(e.target.value)}
               className="w-full rounded-md border-slate-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 py-2 px-3 border"
             >
               {versions.map(v => <option key={v} value={v}>{v.replace('.txt', '').replace(/_/g, ' ')}</option>)}
             </select>
           </div>
           
           <div className="pt-6">
              <ArrowRight className="text-slate-400" />
           </div>

           <div className="flex-1">
             <label className="block text-sm font-medium text-slate-700 mb-1">Comparison Version</label>
             <select 
               value={v2} 
               onChange={(e) => setV2(e.target.value)}
               className="w-full rounded-md border-slate-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 py-2 px-3 border"
             >
               {versions.map(v => <option key={v} value={v}>{v.replace('.txt', '').replace(/_/g, ' ')}</option>)}
             </select>
           </div>
        </div>

        {/* Timeline Visualization */}
        <div className="relative pt-4 pb-8">
           <div className="absolute top-1/2 left-0 w-full h-0.5 bg-slate-100 -translate-y-1/2"></div>
           <div className="relative flex justify-between max-w-2xl mx-auto">
              {versions.map((v, idx) => (
                 <div key={v} className="flex flex-col items-center relative z-10">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-colors ${
                       v === v1 || v === v2 
                         ? 'bg-brand-50 border-brand-500 text-brand-600' 
                         : 'bg-white border-slate-300 text-slate-400'
                    }`}>
                       <GitCommit size={16} />
                    </div>
                    <div className="mt-2 text-xs font-medium text-slate-600 text-center max-w-[100px]">
                       {v.replace('Deal_Delta_', '').replace('.txt', '')}
                    </div>
                    <div className="text-[10px] text-slate-400">
                       {idx === 0 ? 'Oct 2022' : idx === 1 ? 'Mar 2023' : 'Nov 2023'}
                    </div>
                 </div>
              ))}
           </div>
        </div>
      </div>

      {/* Diff Output */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden min-h-[400px]">
         <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex items-center space-x-2">
            <FileDiff size={18} className="text-slate-500" />
            <h3 className="font-semibold text-slate-900">Redline Analysis</h3>
         </div>
         
         <div className="p-6 font-mono text-sm leading-relaxed overflow-x-auto">
            {loading ? (
               <div className="flex flex-col items-center justify-center h-48 space-y-4 text-slate-400">
                  <div className="animate-spin rounded-full h-8 w-8 border-2 border-brand-500 border-t-transparent" />
                  <p>Comparing versions...</p>
               </div>
            ) : diff && diff.changes && diff.changes.length > 0 ? (
               <div className="space-y-1">
                  {diff.changes.map((line: string, i: number) => {
                     let color = 'text-slate-600';
                     let bg = '';
                     if (line.startsWith('+')) {
                        color = 'text-green-700';
                        bg = 'bg-green-50';
                     } else if (line.startsWith('-')) {
                        color = 'text-red-700 decoration-red-900/30 line-through decoration-2';
                        bg = 'bg-red-50 opacity-70';
                     }
                     
                     return (
                        <div key={i} className={`${bg} px-2 py-0.5 rounded-sm`}>
                           <span className={color}>{line}</span>
                        </div>
                     );
                  })}
               </div>
            ) : (
               <div className="text-center text-slate-400 py-12">
                  <p>No differences found or versions identical.</p>
               </div>
            )}
         </div>
      </div>
    </div>
  );
};

export default AmendmentsPage;

