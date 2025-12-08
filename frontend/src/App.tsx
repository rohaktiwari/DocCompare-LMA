import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { ShieldCheck, BarChart3, History, FileText } from 'lucide-react';
import SingleDealPage from './pages/SingleDealPage';
import PortfolioDashboardPage from './pages/PortfolioDashboardPage';
import AmendmentsPage from './pages/AmendmentsPage';

const NavItem = ({ to, icon: Icon, label }: { to: string; icon: any; label: string }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link 
      to={to} 
      className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
        isActive 
          ? 'bg-brand-50 text-brand-600 font-medium' 
          : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
      }`}
    >
      <Icon size={18} />
      <span>{label}</span>
    </Link>
  );
};

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2">
              <div className="bg-brand-600 text-white p-1.5 rounded">
                <ShieldCheck size={24} />
              </div>
              <span className="text-xl font-bold text-slate-900">DocCompare <span className="text-brand-600">LMA</span></span>
            </Link>
            
            <nav className="hidden md:flex space-x-1">
              <NavItem to="/" icon={FileText} label="Single Deal Analysis" />
              <NavItem to="/portfolio" icon={BarChart3} label="Portfolio Dashboard" />
              <NavItem to="/amendments" icon={History} label="Amendment Tracking" />
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
             <div className="text-sm text-slate-500">
                LMA Compliance Assistant v1.0
             </div>
             <div className="h-8 w-8 rounded-full bg-brand-100 flex items-center justify-center text-brand-700 font-bold text-sm border border-brand-200">
                JD
             </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<SingleDealPage />} />
          <Route path="/portfolio" element={<PortfolioDashboardPage />} />
          <Route path="/amendments" element={<AmendmentsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

