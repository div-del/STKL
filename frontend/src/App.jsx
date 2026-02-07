import React, { useState } from 'react';
import SearchHero from './components/SearchHero';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (name, extraInfo) => {
    setLoading(true);
    try {
      // Hardcoded for stability
      const API_BASE = "https://stkl.vercel.app";
      const url = `${API_BASE}/api/search`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, extra_info: extraInfo }),
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search failed:", error);
      alert(`Backend Connection Failed to ${API_BASE}: ${error.message}`);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
  };

  if (loading) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col items-center justify-center w-full h-screen bg-black/70 backdrop-blur-sm">
        <div className="w-24 h-24 border-t-4 border-b-4 border-cyan-500 rounded-full animate-spin mb-8 shadow-[0_0_20px_rgba(6,182,212,0.5)]"></div>
        <p className="animate-pulse text-2xl font-bold tracking-[0.2em] text-cyan-400 font-['Orbitron'] drop-shadow-[0_0_10px_rgba(6,182,212,0.8)]">
          SCANNING GLOBAL NETWORKS...
        </p>
      </div>
    );
  }

  return (
    <div className="w-full min-h-screen flex items-center justify-center overflow-x-hidden">
      {!results ? (
        <SearchHero onSearch={handleSearch} />
      ) : (
        <ResultsDashboard results={results} onReset={handleReset} />
      )}
    </div>
  );
}

export default App;
