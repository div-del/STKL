import React, { useState } from 'react';
import SearchHero from './components/SearchHero';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (name, extraInfo) => {
    setLoading(true);
    try {
      // In production, use env variable for API URL
      const url = '/api/search';
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
      alert(`Backend Connection Failed to http://localhost:8001: ${error.message}`);
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
      <div className="min-h-screen bg-black flex flex-col items-center justify-center text-green-500 font-mono">
        <div className="w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="animate-pulse">SCANNING GLOBAL NETWORKS...</p>
      </div>
    );
  }

  return (
    <div>
      {!results ? (
        <SearchHero onSearch={handleSearch} />
      ) : (
        <ResultsDashboard results={results} onReset={handleReset} />
      )}
    </div>
  );
}

export default App;
